
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="10초 맞추기",
    layout="wide"
)

html_code = r"""

<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>10초 타이머 게임</title>

  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      background: #10131c;
      color: white;
      font-family: Arial, sans-serif;
      user-select: none;
    }

    .game {
      width: 100%;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 24px;
      text-align: center;
      cursor: pointer;
    }

    h1 {
      font-size: 26px;
      color: #aeb8d0;
      margin-bottom: 18px;
    }

    .timer {
      font-size: clamp(64px, 16vw, 120px);
      font-weight: bold;
      font-variant-numeric: tabular-nums;
      letter-spacing: -3px;
      color: #ffffff;
      margin: 20px 0;
    }

    /* 5초가 지나면 타이머 숫자 숨기기 */
    .timer.hidden {
      visibility: hidden;
    }

    .message {
      font-size: 17px;
      color: #9da8c0;
      line-height: 1.8;
    }

    .result {
      display: none;
      margin-top: 22px;
    }

    .final-time {
      font-size: 22px;
      color: #ffffff;
      margin-bottom: 12px;
    }

    .result-label {
      font-size: 16px;
      color: #aeb8d0;
      margin-bottom: 8px;
    }

    .error {
      font-size: 34px;
      font-weight: bold;
      color: #66e3b4;
      margin: 10px 0 24px;
    }

    button {
      cursor: pointer;
      border: none;
      border-radius: 12px;
      padding: 14px 38px;
      background: #6c7cff;
      color: white;
      font-size: 18px;
      font-weight: bold;
    }

    button:hover {
      background: #8491ff;
    }

    .game.running .timer {
      color: #7cddff;
    }

    .game.finished {
      cursor: default;
    }

    .target {
      font-size: 14px;
      color: #68748e;
      margin-top: 28px;
    }
  </style>
</head>

<body>
  <main class="game" id="game">

    <h1>10초 타이머 게임</h1>

    <div class="timer" id="timer">0.000</div>

    <div class="message" id="message">
      화면을 클릭해서 시작하세요.<br>
      5초가 지나면 타이머가 사라집니다!<br>
      속으로 시간을 세다가 10초에 맞춰 클릭하세요.
    </div>

    <div class="result" id="result">

      <div class="final-time">
        측정 시간: <span id="finalTime">0.000</span>초
      </div>

      <div class="result-label">
        10.000초와의 오차
      </div>

      <div class="error" id="error">0.000초</div>

      <button id="restart">다시 하기</button>
    </div>

    <div class="target">TARGET · 10.000 SEC</div>

  </main>

  <script>
    const game = document.getElementById("game");
    const timer = document.getElementById("timer");
    const message = document.getElementById("message");
    const result = document.getElementById("result");
    const finalTime = document.getElementById("finalTime");
    const error = document.getElementById("error");
    const restart = document.getElementById("restart");

    const TARGET = 10.000;
    const HIDE_TIME = 5.000;

    let startTime = 0;
    let animationId = null;
    let state = "ready";

    // 소수점 셋째 자리까지 표시
    function formatTime(seconds) {
      return seconds.toFixed(3);
    }

    // 타이머 업데이트
    function updateTimer() {
      if (state !== "running") return;

      const elapsed = (performance.now() - startTime) / 1000;

      timer.textContent = formatTime(elapsed);

      // 5.000초가 되면 숫자 숨기기
      if (elapsed >= HIDE_TIME) {
        timer.classList.add("hidden");
      }

      // 숫자가 숨겨져도 측정은 계속 진행
      animationId = requestAnimationFrame(updateTimer);
    }

    // 게임 시작
    function startGame() {
      state = "running";
      startTime = performance.now();

      timer.textContent = "0.000";
      timer.classList.remove("hidden");

      game.classList.add("running");

      message.innerHTML =
        "타이머가 시작되었습니다!<br>" +
        "5초 이후에는 속으로 시간을 세어 보세요.";

      result.style.display = "none";

      updateTimer();
    }

    // 타이머 정지 및 결과 계산
    function stopGame() {
      // 실제 경과 시간을 정밀하게 측정
      const elapsed = (performance.now() - startTime) / 1000;
      const difference = Math.abs(elapsed - TARGET);

      state = "finished";

      cancelAnimationFrame(animationId);

      // 최종 결과를 보여주기 위해 숫자 다시 표시
      timer.classList.remove("hidden");
      timer.textContent = formatTime(elapsed);

      finalTime.textContent = formatTime(elapsed);
      error.textContent = formatTime(difference) + "초";

      // 결과 메시지
      if (difference < 0.0005) {
        message.textContent = "완벽합니다! 정확히 10초입니다!";
      } else if (difference < 0.050) {
        message.textContent = "대단해요! 거의 정확합니다!";
      } else if (elapsed < TARGET) {
        message.textContent = "조금 빨랐어요!";
      } else {
        message.textContent = "조금 늦었어요!";
      }

      // 오차에 따라 색상 변경
      if (difference < 0.050) {
        error.style.color = "#66e3b4";
      } else if (difference < 0.200) {
        error.style.color = "#ffd166";
      } else {
        error.style.color = "#ff7676";
      }

      game.classList.remove("running");
      game.classList.add("finished");

      result.style.display = "block";
    }

    // 화면 클릭으로 시작하거나 정지
    game.addEventListener("click", (event) => {
      // 버튼 클릭은 게임 화면 클릭으로 처리하지 않음
      if (event.target.closest("button")) return;

      if (state === "ready") {
        startGame();
      } else if (state === "running") {
        stopGame();
      }
    });

    // 다시 하기 버튼
    restart.addEventListener("click", () => {
      cancelAnimationFrame(animationId);

      state = "ready";
      startTime = 0;

      timer.textContent = "0.000";
      timer.classList.remove("hidden");

      message.innerHTML =
        "화면을 클릭해서 시작하세요.<br>" +
        "5초가 지나면 타이머가 사라집니다!<br>" +
        "속으로 시간을 세다가 10초에 맞춰 클릭하세요.";

      finalTime.textContent = "0.000";
      error.textContent = "0.000초";
      error.style.color = "#66e3b4";

      result.style.display = "none";

      game.classList.remove("running", "finished");
    });
  </script>
</body>
</html>

"""

components.html(
    html_code,
    height=650,
    scrolling=True
)
