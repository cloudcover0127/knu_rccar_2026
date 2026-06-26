let isPowerOn = false;   
let currentSpeed = 0;
let targetSpeed = 0;
let steerAngle = 0;      
let driveState = 'stop'; 
let speedTimer = null;

let activeControls = { forward: false, backward: false, left: false, right: false };

// 🔘 1. 시동 버튼 제어
function togglePower() {
    isPowerOn = !isPowerOn;
    
    const btn = document.getElementById('powerBtn');
    const statusText = document.getElementById('sysStatus');
    const speedNum = document.getElementById('speedNum');

    if (isPowerOn) {
        btn.classList.add('engine-on');
        document.body.classList.add('sys-active');
        statusText.innerText = "🟢 SYSTEM ONLINE";
        statusText.style.color = "#10b981";
        speedNum.classList.add('active');
        calculatePhysics(); 
        log("ENGINE START. USE WHEEL TO STEER.");
    } else {
        emergencyStop(); 
        btn.classList.remove('engine-on');
        document.body.classList.remove('sys-active');
        statusText.innerText = "🔴 SYSTEM OFF";
        statusText.style.color = "#ef4444";
        speedNum.classList.remove('active');
        log("ENGINE SHUTDOWN. SYSTEM OFF.");
    }
}

// 🕹️ 2. 마우스 누름/뗌 페달 제어 함수
function pedalControl(action, isPressed) {
    if (!isPowerOn) return; 

    if (action === 'forward') {
        activeControls['forward'] = isPressed;
        if (isPressed) activeControls['backward'] = false;
    } else if (action === 'backward') {
        activeControls['backward'] = isPressed;
        if (isPressed) activeControls['forward'] = false;
    }

    if (activeControls['forward']) driveState = 'forward';
    else if (activeControls['backward']) driveState = 'backward';
    else driveState = 'stop';

    calculatePhysics(); // 물리 엔진 즉시 트리거
    sendSignal();
}

// 🔄 3. [최종 업그레이드] 마우스 휠 조향 (실제 핸들 회전 연동)
window.addEventListener('wheel', function(event) {
    if (!isPowerOn) return;
    event.preventDefault(); 

    // deltaY가 양수면 오른쪽, 음수면 왼쪽
    if (event.deltaY > 0) steerAngle += 15;  // 15도씩 부드럽게 회전
    else steerAngle -= 15;                 

    // 최대 회전 각도 제한 (-180도 ~ 180도, 진짜 운전 느낌)
    if (steerAngle < -180) steerAngle = -180;
    if (steerAngle > 180) steerAngle = 180;

    calculatePhysics(); // 코너링 감속 적용
    sendSignal();
}, { passive: false });

// 🛠️ 조향 초기화 함수 (RESET 버튼)
function resetSteer() {
    if (!isPowerOn) return;
    steerAngle = 0;
    calculatePhysics();
    sendSignal();
}

// ⚙️ 4. 가속 / 관성 감속 물리 엔진
function calculatePhysics() {
    clearInterval(speedTimer);

    speedTimer = setInterval(function() {
        if (!isPowerOn) {
            clearInterval(speedTimer);
            return;
        }

        if (driveState === 'stop') {
            targetSpeed = 0;
        } else {
            targetSpeed = 80; 
            // 핸들이 많이 꺾일수록 부드럽게 감속 저항 적용 (소수점 원천 방지)
            let steerFactor = Math.abs(steerAngle) / 180; // 0.0 ~ 1.0
            if (steerFactor > 0.1) {
                targetSpeed = Math.round(80 - (steerFactor * 30)); // 최대 30km 감속
            }
        }

        if (currentSpeed < targetSpeed) {
            currentSpeed += 5; 
        } else if (currentSpeed > targetSpeed) {
            currentSpeed -= (driveState === 'stop') ? 4 : 8; 
        }

        if (Math.abs(currentSpeed - targetSpeed) < 4) currentSpeed = targetSpeed;
        if (currentSpeed < 0) currentSpeed = 0;

        updateUI();
    }, 40);
}

// 🎨 5. UI 및 실시간 핸들 회전 갱신
function updateUI() {
    document.getElementById('speedNum').innerText = Math.round(currentSpeed);

    let gear = 'PARK ■';
    if (!isPowerOn) gear = 'READY';
    else if (driveState === 'forward') gear = 'DRIVE ▲';
    else if (driveState === 'backward') gear = 'REVERSE ▼';
    else if (driveState === 'stop' && currentSpeed > 0) gear = 'BRAKE ⚠️';
    document.getElementById('gearText').innerText = gear;

    // 🔄 [핵심] 실제 핸들(스티어링 휠) 아이콘 회전 시키기
    const wheel = document.getElementById('steeringWheel');
    // steerAngle(-180 ~ 180도) 값을 CSS transform: rotate()에 그대로 적용
    wheel.style.transform = `rotate(${steerAngle}deg)`;

    document.querySelector('.btn-up').classList.toggle('active', activeControls['forward']);
    document.querySelector('.btn-down').classList.toggle('active', activeControls['backward']);
    
    // 조향 버튼 하이라이트 (Reset 버튼으로 용도 변경)
    document.querySelector('.btn-left').classList.toggle('active', steerAngle < -15);
    document.querySelector('.btn-right').classList.toggle('active', steerAngle > 15);

    // 하단 영문 로그 (조향 신호는 -1.0 ~ 1.0 포맷으로 서버 전송)
    let steerSignal = (steerAngle / 180).toFixed(2);
    log(`GEAR: ${gear.replace(' ■','').replace(' ▲','').replace(' ▼','').replace(' ⚠️','')} | STEER: ${steerSignal} | SPEED: ${Math.round(currentSpeed)}KM/H`);
}

function emergencyStop() {
    driveState = 'stop';
    steerAngle = 0;
    currentSpeed = 0;
    activeControls['forward'] = false;
    activeControls['backward'] = false;
    updateUI();
    fetch('/move/stop');
}

function sendSignal() {
    // 서버로는 실제 각도 대신 -1.0 ~ 1.0 범위의 조향 신호를 보냅니다.
    let steerSignal = (steerAngle / 180).toFixed(2);
    fetch(`/move/${driveState}?steer=${steerSignal}`);
}

function log(msg) {
    document.getElementById('consoleLog').innerText = `> ${msg}`;
}

// 키보드 엔터(핸들 초기화) 및 스페이스바(비상정지) 호환
window.addEventListener('keydown', function(event) {
    if (!isPowerOn) return;
    if (event.key === ' ') { event.preventDefault(); emergencyStop(); }
    if (event.key === 'Enter') { resetSteer(); }
});