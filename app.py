
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="10초 맞추기",
    layout="wide"
)

html_code = r"""

```html
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
      background: #ffffff;
      color: #29466f;
      font-family: Arial, "Malgun Gothic", sans-serif;
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
      font-size: clamp(24px, 5vw, 36px);
      font-weight: 800;
      color: #29466f;
      margin: 0 0 20px;
    }

    .timer {
      font-size: clamp(64px, 16vw, 120px);
      font-weight: bold;
      font-variant-numeric: tabular-nums;
      letter-spacing: -3px;
      color: #315784;
      margin: 12px 0 20px;
    }

    /* 5초가 지나면 타이머 숫자 숨기기 */
    .timer.hidden {
      visibility: hidden;
    }

    .message {
      font-size: clamp(15px, 3vw, 18px);
      color: #58749b;
      line-height: 1.9;
      background: #f0f6ff;
      border-radius: 24px;
      padding: 18px 28px;
      width: min(100%, 600px);
      min-height: 100px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    .result {
      display: none;
      width: min(100%, 400px);
      margin-top: 24px;
      padding: 24px;
      border: 2px solid #e0edff;
      border-radius: 24px;
      background: #ffffff;
    }

    .final-time {
      font-size: 22px;
      font-weight: bold;
      color: #315784;
      margin-bottom: 20px;
    }

    .result-label {
      font-size: 16px;
      color: #7189a9;
      margin-bottom: 10px;
    }

    .error {
      font-size: clamp(28px, 7vw, 36px);
      font-weight: bold;
      color: #20b695;
      margin: 10px 0 24px;
    }

    button {
      cursor: pointer;
      border: none;
      border-radius: 14px;
      padding: 15px 36px;
      width: 100%;
      max-width: 260px;
      background: #4d8cf5;
      color: white;
      font-size: 18px;
      font-weight: bold;
      transition: background 0.2s, transform 0.2s;
    }

    button:hover {
      background: #3677e8;
      transform: translateY(-2px);
    }

    button:active {
      transform: scale(0.98);
    }

    .game.running .timer {
      color: #4d8cf5;
    }

    .game.finished {
      cursor: default;
    }

    .target {
      font-size: 14px;
      font-weight: bold;
      color: #8499b8;
      margin-top: 24px;
      letter-spacing: 0.5px;
    }

    @media (max-width: 480px) {
      .game {
        padding: 20px;
      }

      .message {
        padding: 16px;
      }

      .result {
        padding: 20px;
      }
    }
  </style>
</head>

<body>
  <main class="game" id="game">

    <h1>10초 타이머 게임</h1>

    <div class="timer" id="timer">0.000</div>

    <div class="message" id="message">
      <div>화면을 클릭해서 시작하세요.</div>
      <div>5초가 지나면 타이머가 사라집니다!</div>
      <div>속으로 시간을 세다가 10초에 맞춰 클릭하세요.</div>
    </div>

    <div class="result" id="result">

      <div class="final-time">
        <div class="result-label">측정 시간</div>
        <span id="finalTime">0.000</span>초
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

      // 5초가 지나면 숫자 숨기기
      if (elapsed >= HIDE_TIME) {
        timer.classList.add("hidden");
      }

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
        "<div>타이머가 시작되었습니다!</div>" +
        "<div>5초 이후에는 속으로 시간을 세어 보세요.</div>";

      result.style.display = "none";

      updateTimer();
    }

    // 게임 종료 및 결과 계산
    function stopGame() {
      const elapsed = (performance.now() - startTime) / 1000;
      const difference = Math.abs(elapsed - TARGET);

      state = "finished";

      cancelAnimationFrame(animationId);

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
        error.style.color = "#20b695";
      } else if (difference < 0.200) {
        error.style.color = "#e5a52e";
      } else {
        error.style.color = "#ed6b75";
      }

      game.classList.remove("running");
      game.classList.add("finished");

      result.style.display = "block";
    }

    // 화면을 클릭해서 시작하거나 정지
    game.addEventListener("click", (event) => {
      if (event.target.closest("button")) return;

      if (state === "ready") {
        startGame();
      } else if (state === "running") {
        stopGame();
      }
    });

    // 다시 하기
    restart.addEventListener("click", () => {
      cancelAnimationFrame(animationId);

      state = "ready";
      startTime = 0;

      timer.textContent = "0.000";
      timer.classList.remove("hidden");

      message.innerHTML =
        "<div>화면을 클릭해서 시작하세요.</div>" +
        "<div>5초가 지나면 타이머가 사라집니다!</div>" +
        "<div>속으로 시간을 세다가 10초에 맞춰 클릭하세요.</div>";

      finalTime.textContent = "0.000";
      error.textContent = "0.000초";
      error.style.color = "#20b695";

      result.style.display = "none";

      game.classList.remove("running", "finished");
    });
  </script>
</body>
</html>
```
"""

components.html(
    html_code,
    height=650,
    scrolling=True
)
