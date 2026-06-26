let isPowerOn = false;   
let currentSpeed = 0;
let targetSpeed = 0;
let steerAngle = 0;      
let driveState = 'stop'; 
let speedTimer = null;

let activeControls = { forward: false, backward: false };

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
        log("ENGINE START. READY TO DRIVE.");
        calculatePhysics(); 
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

    sendTargetSignal();
}

// 🌀 3. 마우스 휠 조향
window.addEventListener('wheel', function(event) {
    if (!isPowerOn) return;
    event.preventDefault(); 

    if (event.deltaY > 0) steerAngle += 5;  
    else steerAngle -= 5;                 

    if (steerAngle < -45) steerAngle = -45;
    if (steerAngle > 45) steerAngle = 45;

    sendTargetSignal();
}, { passive: false });

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
            if (Math.abs(steerAngle) > 0) {
                targetSpeed = Math.round(80 - (Math.abs(steerAngle) * 0.6)); 
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

// 🎨 5. UI 및 대미 장식 영문 로그 포맷팅 갱신
function updateUI() {
    document.getElementById('speedNum').innerText = Math.round(currentSpeed);

    let gear = 'PARK ■';
    if (!isPowerOn) gear = 'READY';
    else if (driveState === 'forward') gear = 'DRIVE ▲';
    else if (driveState === 'backward') gear = 'REVERSE ▼';
    else if (driveState === 'stop' && currentSpeed > 0) gear = 'BRAKE ⚠️';
    document.getElementById('gearText').innerText = gear;

    let steerText = 'STEER: 0°';
    if (steerAngle < 0) steerText = `STEER: ${Math.round(steerAngle)}° (L)`;
    if (steerAngle > 0) steerText = `STEER: +${Math.round(steerAngle)}° (R)`;
    document.getElementById('steerText').innerText = steerText;

    document.querySelector('.btn-up').classList.toggle('active', activeControls['forward']);
    document.querySelector('.btn-down').classList.toggle('active', activeControls['backward']);
    document.querySelector('.btn-left').classList.toggle('active', steerAngle < -10);
    document.querySelector('.btn-right').classList.toggle('active', steerAngle > 10);

    // 하단 짜침 해방 고해상도 영문 포맷 로그
    let cleanGear = gear.replace(' ■','').replace(' ▲','').replace(' ▼','').replace(' ⚠️','');
    log(`GEAR: ${cleanGear} | STEER: ${Math.round(steerAngle)}° | SPEED: ${Math.round(currentSpeed)}KM/H`);
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

function sendTargetSignal() {
    fetch(`/move/${driveState}?steer=${Math.round(steerAngle)}`);
}

function log(msg) {
    document.getElementById('consoleLog').innerText = `> ${msg}`;
}

window.addEventListener('keydown', function(event) {
    if (!isPowerOn) return;
    if (event.key === ' ') { event.preventDefault(); emergencyStop(); }
    if (event.key === 'Enter') { steerAngle = 0; sendTargetSignal(); }
});