function sendCommand(direction) {
    // 지정된 방향 주소로 웹 페이지를 이동시킵니다 (예: /move/forward)
    location.href = '/move/' + direction;
}