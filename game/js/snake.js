// 贪吃蛇游戏逻辑
document.addEventListener('DOMContentLoaded', function() {
  // 游戏元素
  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');
  const startBtn = document.getElementById('startBtn');
  const pauseBtn = document.getElementById('pauseBtn');
  const restartBtn = document.getElementById('restartBtn');
  const startFromHereBtn = document.getElementById('startFromHereBtn');
  const playAgainBtn = document.getElementById('playAgainBtn');
  const scoreElement = document.getElementById('score');
  const lengthElement = document.getElementById('length');
  const highScoreElement = document.getElementById('highScore');
  const speedElement = document.getElementById('speed');
  const finalScoreElement = document.getElementById('finalScore');
  const gameOverElement = document.getElementById('gameOver');
  const gameStartElement = document.getElementById('gameStart');
  
  // 游戏参数
  const gridSize = 20;
  const gridWidth = canvas.width / gridSize;
  const gridHeight = canvas.height / gridSize;
  
  // 游戏状态
  let snake = [];
  let food = {};
  let direction = 'right';
  let nextDirection = 'right';
  let score = 0;
  let highScore = localStorage.getItem('snakeHighScore') || 0;
  let gameSpeed = 150; // 初始速度（毫秒）
  let gameInterval;
  let isPaused = false;
  let isGameOver = false;
  let isGameStarted = false;
  
  // 初始化游戏
  function initGame() {
    // 初始化蛇
    snake = [
      {x: 5, y: 10},
      {x: 4, y: 10},
      {x: 3, y: 10}
    ];
    
    // 生成食物
    generateFood();
    
    // 重置游戏状态
    direction = 'right';
    nextDirection = 'right';
    score = 0;
    gameSpeed = 150;
    isGameOver = false;
    isGameStarted = false;
    
    // 更新UI
    updateUI();
    
    // 显示开始界面
    gameStartElement.style.display = 'flex';
    gameOverElement.style.display = 'none';
    
    // 绘制初始状态
    draw();
  }
  
  // 生成食物
  function generateFood() {
    // 确保食物不会出现在蛇身上
    let foodOnSnake;
    do {
      foodOnSnake = false;
      food = {
        x: Math.floor(Math.random() * gridWidth),
        y: Math.floor(Math.random() * gridHeight)
      };
      
      // 检查食物是否在蛇身上
      for (let segment of snake) {
        if (segment.x === food.x && segment.y === food.y) {
          foodOnSnake = true;
          break;
        }
      }
    } while (foodOnSnake);
  }
  
  // 绘制游戏
  function draw() {
    // 清空画布
    ctx.fillStyle = '#2c3e50';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // 绘制网格
    drawGrid();
    
    // 绘制蛇
    for (let i = 0; i < snake.length; i++) {
      // 蛇头
      if (i === 0) {
        ctx.fillStyle = '#27ae60'; // 头部颜色
      } else {
        // 蛇身渐变
        const alpha = 0.7 - (i / snake.length) * 0.5;
        ctx.fillStyle = `rgba(39, 174, 96, ${alpha})`;
      }
      
      ctx.fillRect(
        snake[i].x * gridSize,
        snake[i].y * gridSize,
        gridSize - 2,
        gridSize - 2
      );
      
      // 蛇身圆角
      ctx.fillStyle = i === 0 ? '#2ecc71' : '#219653';
      ctx.beginPath();
      ctx.arc(
        snake[i].x * gridSize + gridSize/2,
        snake[i].y * gridSize + gridSize/2,
        gridSize/2 - 2,
        0,
        Math.PI * 2
      );
      ctx.fill();
      
      // 蛇眼睛（只在头部）
      if (i === 0) {
        ctx.fillStyle = 'white';
        // 根据方向确定眼睛位置
        let eyeOffsetX = 0, eyeOffsetY = 0;
        switch(direction) {
          case 'right': eyeOffsetX = 3; break;
          case 'left': eyeOffsetX = -3; break;
          case 'up': eyeOffsetY = -3; break;
          case 'down': eyeOffsetY = 3; break;
        }
        
        ctx.beginPath();
        ctx.arc(
          snake[i].x * gridSize + gridSize/2 - eyeOffsetX,
          snake[i].y * gridSize + gridSize/2 - eyeOffsetY,
          2,
          0,
          Math.PI * 2
        );
        ctx.fill();
        
        ctx.beginPath();
        ctx.arc(
          snake[i].x * gridSize + gridSize/2 + eyeOffsetX,
          snake[i].y * gridSize + gridSize/2 + eyeOffsetY,
          2,
          0,
          Math.PI * 2
        );
        ctx.fill();
      }
    }
    
    // 绘制食物
    ctx.fillStyle = '#e74c3c';
    ctx.beginPath();
    ctx.arc(
      food.x * gridSize + gridSize/2,
      food.y * gridSize + gridSize/2,
      gridSize/2 - 2,
      0,
      Math.PI * 2
    );
    ctx.fill();
    
    // 食物光泽效果
    ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
    ctx.beginPath();
    ctx.arc(
      food.x * gridSize + gridSize/2 - 3,
      food.y * gridSize + gridSize/2 - 3,
      3,
      0,
      Math.PI * 2
    );
    ctx.fill();
  }
  
  // 绘制网格
  function drawGrid() {
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    
    // 垂直线
    for (let x = 0; x <= canvas.width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvas.height);
      ctx.stroke();
    }
    
    // 水平线
    for (let y = 0; y <= canvas.height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(canvas.width, y);
      ctx.stroke();
    }
  }
  
  // 更新游戏状态
  function update() {
    // 更新方向
    direction = nextDirection;
    
    // 计算新的蛇头位置
    const head = {...snake[0]};
    
    switch(direction) {
      case 'up': head.y--; break;
      case 'down': head.y++; break;
      case 'left': head.x--; break;
      case 'right': head.x++; break;
    }
    
    // 检查游戏结束条件
    // 1. 撞墙
    if (head.x < 0 || head.x >= gridWidth || head.y < 0 || head.y >= gridHeight) {
      gameOver();
      return;
    }
    
    // 2. 撞到自己
    for (let segment of snake) {
      if (head.x === segment.x && head.y === segment.y) {
        gameOver();
        return;
      }
    }
    
    // 移动蛇
    snake.unshift(head);
    
    // 检查是否吃到食物
    if (head.x === food.x && head.y === food.y) {
      // 增加分数
      score += 10;
      
      // 每吃10个食物增加速度
      if (score % 100 === 0 && gameSpeed > 50) {
        gameSpeed -= 20;
        clearInterval(gameInterval);
        gameInterval = setInterval(gameLoop, gameSpeed);
        updateSpeedDisplay();
      }
      
      // 生成新食物
      generateFood();
      
      // 更新UI
      updateUI();
    } else {
      // 如果没有吃到食物，移除尾部
      snake.pop();
    }
    
    // 更新长度显示
    lengthElement.textContent = snake.length;
  }
  
  // 游戏循环
  function gameLoop() {
    if (!isPaused && !isGameOver && isGameStarted) {
      update();
      draw();
    }
  }
  
  // 游戏结束
  function gameOver() {
    isGameOver = true;
    isGameStarted = false;
    
    // 更新最高分
    if (score > highScore) {
      highScore = score;
      localStorage.setItem('snakeHighScore', highScore);
      highScoreElement.textContent = highScore;
    }
    
    // 显示游戏结束界面
    finalScoreElement.textContent = score;
    gameOverElement.style.display = 'flex';
    
    // 停止游戏循环
    clearInterval(gameInterval);
  }
  
  // 更新UI显示
  function updateUI() {
    scoreElement.textContent = score;
    lengthElement.textContent = snake.length;
    highScoreElement.textContent = highScore;
  }
  
  // 更新速度显示
  function updateSpeedDisplay() {
    if (gameSpeed >= 130) {
      speedElement.textContent = '慢速';
    } else if (gameSpeed >= 90) {
      speedElement.textContent = '正常';
    } else if (gameSpeed >= 60) {
      speedElement.textContent = '快速';
    } else {
      speedElement.textContent = '极速';
    }
  }
  
  // 开始游戏
  function startGame() {
    if (!isGameStarted) {
      isGameStarted = true;
      isPaused = false;
      gameStartElement.style.display = 'none';
      gameOverElement.style.display = 'none';
      
      // 启动游戏循环
      gameInterval = setInterval(gameLoop, gameSpeed);
      updateSpeedDisplay();
    }
  }
  
  // 暂停游戏
  function pauseGame() {
    if (isGameStarted && !isGameOver) {
      isPaused = !isPaused;
      pauseBtn.textContent = isPaused ? '继续' : '暂停';
    }
  }
  
  // 重新开始游戏
  function restartGame() {
    clearInterval(gameInterval);
    initGame();
    pauseBtn.textContent = '暂停';
  }
  
  // 键盘控制
  document.addEventListener('keydown', function(event) {
    // 空格键暂停/继续
    if (event.code === 'Space') {
      event.preventDefault();
      pauseGame();
      return;
    }
    
    // 方向键控制
    switch(event.key) {
      case 'ArrowUp':
        if (direction !== 'down') nextDirection = 'up';
        break;
      case 'ArrowDown':
        if (direction !== 'up') nextDirection = 'down';
        break;
      case 'ArrowLeft':
        if (direction !== 'right') nextDirection = 'left';
        break;
      case 'ArrowRight':
        if (direction !== 'left') nextDirection = 'right';
        break;
    }
  });
  
  // 按钮事件监听
  startBtn.addEventListener('click', startGame);
  pauseBtn.addEventListener('click', pauseGame);
  restartBtn.addEventListener('click', restartGame);
  startFromHereBtn.addEventListener('click', startGame);
  playAgainBtn.addEventListener('click', restartGame);
  
  // 初始化游戏
  initGame();
  updateUI();
});