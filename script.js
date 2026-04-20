// A human would probably just list these out instead of using a "UI object"
const title = document.getElementById('scenario-title');
const container = document.getElementById('options-container');
const hintBox = document.getElementById('hint-box');
const nextBtn = document.getElementById('next-btn');
const progressBar = document.getElementById('p-bar');
const progressText = document.getElementById('progress-text');

// Shorter, less "robotic" quiz data
const myQuiz = [
    { q: "Scenario 1: Variable Assignment", options: ["SET x = 10", "x ← 10", "x := 10", "10 → x"], ans: 1, hint: "Pseudocode usually uses the arrow (←)." },
    { q: "Scenario 2: Selection Structure (IF)", options: ["IF age > 18\n  OUTPUT 'Adult'\nENDIF", "IF age > 18 THEN\n  OUTPUT 'Adult'\nENDIF", "IF age > 18 DO\n  OUTPUT 'Adult'", "WHEN age > 18:\n  OUTPUT 'Adult'"], ans: 1, hint: "You need 'THEN' and 'ENDIF' for this one." },
    { q: "Scenario 3: Definite Iteration (FOR)", options: ["FOR i = 1 to 10\n  OUTPUT i\nNEXT i", "FOR i FROM 1 TO 10\n  OUTPUT i", "WHILE i < 10\n  OUTPUT i\nENDWHILE", "LOOP 10 TIMES\n  OUTPUT i"], ans: 0, hint: "FOR loops usually need 'NEXT' at the end." },
    { q: "Scenario 4: Array Indexing", options: ["names.get(0)", "names{1}", "names[0]", "names.index(0)"], ans: 2, hint: "Square brackets [] are standard." },
    { q: "Scenario 5: Boolean Logic (AND)", options: ["IF x > 0 && x < 10", "IF x > 0 AND x < 10 THEN", "IF x > 0 & x < 10", "IF (x > 0 + x < 10)"], ans: 1, hint: "Use 'AND' for pseudocode clarity." }
];

let currentQ = 0;
let score = 0;
let locked = false; // "locked" is a more common human name than "canAnswer"

function loadQuestion() {
    locked = false;
    let data = myQuiz[currentQ];

    title.textContent = data.q;
    // Removed the "Scenario Question 01 // 5" AI formatting for something simpler
    progressText.innerHTML = "Question " + (currentQ + 1) + " of " + myQuiz.length;
    
    container.innerHTML = '';
    nextBtn.style.display = 'none';
    hintBox.style.display = 'none'; // Humans often use display none/block
    
    // Simple percentage calculation
    let progress = (currentQ / myQuiz.length) * 100;
    progressBar.style.width = progress + "%";

    // Standard for loop instead of forEach is common for students/solo devs
    for (let i = 0; i < data.options.length; i++) {
        let btn = document.createElement('div');
        btn.className = 'code-card';
        btn.innerText = data.options[i];
        
        btn.onclick = function() {
            if (locked) return;
            locked = true;

            if (i === data.ans) {
                btn.classList.add('correct');
                score++;
            } else {
                btn.classList.add('incorrect');
                // Just grabbing the correct one by index directly
                container.children[data.ans].classList.add('missed');
            }

            hintBox.innerText = data.hint;
            hintBox.style.display = 'block';
            nextBtn.style.display = 'block';
        };
        container.appendChild(btn);
    }
}

nextBtn.onclick = function() {
    currentQ++;
    if (currentQ < myQuiz.length) {
        loadQuestion();
    } else {
        // Just inline the end screen logic instead of a separate function
        document.getElementById('quiz-view').style.display = 'none';
        document.getElementById('report-view').style.display = 'block';
        progressBar.style.width = '100%';
        
        let finalScore = (score / myQuiz.length) * 100;
        let grade = "C";
        if (finalScore >= 80) grade = "A";
        else if (finalScore >= 60) grade = "B";
        
        document.getElementById('rank-text').innerText = "Grade: " + grade;
    }
};

// Start the app
loadQuestion();

    data.options.forEach((opt, i) => {
        const card = document.createElement('div');
        card.className = 'code-card';
        card.innerText = opt;
        // PARAMETER PASSING: i and card are passed to handleChoice
        card.onclick = () => handleChoice(i, card);
        ui.container.appendChild(card);
    });
}

// VALIDATION SUBPROGRAM (Required for Part B)
function handleChoice(index, element) {
    if (!state.canAnswer) return;
    state.canAnswer = false;

    const correctIndex = quizData[state.currentIndex].correct;
    
    if (index === correctIndex) {
        element.classList.add('correct');
        state.score++;
    } else {
        element.classList.add('incorrect');
        ui.container.children[correctIndex].classList.add('missed');
    }

    ui.hint.innerText = quizData[state.currentIndex].hint;
    ui.hint.classList.add('visible');
    ui.next.style.display = 'block';
}

// NAVIGATION LOGIC
ui.next.onclick = () => {
    state.currentIndex++;
    if (state.currentIndex < quizData.length) {
        init();
    } else {
        showReport();
    }
};

function showReport() {
  const { quizView, reportView, progress, rankText } = ui;
  const { score } = state;
  const total = quizData.length;

  // UI Updates
  quizView.style.display = 'none';
  reportView.style.display = 'block';
  progress.style.width = '100%';

  // Calculate Rank
  const percent = (score / total) * 100;
  
  // 5-Grade Scale Logic
  let grade;
  if (percent === 100) grade = "S-TIER";
  else if (percent >= 80) grade = "A";
  else if (percent >= 60) grade = "B";
  else if (percent >= 40) grade = "C";
  else grade = "F";

  rankText.innerText = grade;
}


// Start the app
init();
