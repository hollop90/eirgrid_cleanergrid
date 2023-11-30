
const homeBtn = document.getElementById("home-btn");
const quizBtn = document.getElementById("quiz-btn");
const energyBtn = document.getElementById("energy-btn");
const startQuizBtn = document.getElementById("start-quiz-btn");
const dashboardBtn = document.getElementById("dashboard-btn");
const communityBtn = document.getElementById("community-btn");

const homeSection = document.getElementById("home-section");
const quizSection = document.getElementById("quiz-section");
const energySection = document.getElementById("energy-section");
const displayQuestion = document.getElementById("display-question");

const dashboardSection = document.getElementById("dashboard-section");
const communitySection = document.getElementById("community-section");

homeBtn.addEventListener("click", function showHomeTab() {
    homeSection.style.display = "block";
    quizSection.style.display = "none";
    energySection.style.display = "none";
    displayQuestion.style.display = "none";
    energySteps.style.display = "none";
    dashboardSection.style.display = "none";
    communitySection.style.display = "none";
})

quizBtn.addEventListener("click", function showQuizTab() {
    homeSection.style.display = "none";
    quizSection.style.display = "block";
    energySection.style.display = "none";
    displayQuestion.style.display = "none";
    energySteps.style.display = "none";
    dashboardSection.style.display = "none";
    communitySection.style.display = "none";
})  

energyBtn.addEventListener("click", function showEnergyTab() {
    homeSection.style.display = "none";
    quizSection.style.display = "none";
    energySection.style.display = "block";
    displayQuestion.style.display = "none";
    energySteps.style.display = "none";
    dashboardSection.style.display = "none";
    communitySection.style.display = "none";
})

dashboardBtn.addEventListener("click", function(){
    homeSection.style.display = "none";
    quizSection.style.display = "none";
    energySection.style.display = "none";
    displayQuestion.style.display = "none";
    energySteps.style.display = "none";
    communitySection.style.display = "none";
    dashboardSection.style.display = "block";

})

communityBtn.addEventListener("click", function(){
    homeSection.style.display = "none";
    quizSection.style.display = "none";
    energySection.style.display = "none";
    displayQuestion.style.display = "none";
    energySteps.style.display = "none";
    dashboardSection.style.display = "none";
    communitySection.style.display = "block";
})


startQuizBtn.addEventListener("click", function displayQuestion() {
    document.getElementById("display-question").style.display = "block";
    document.getElementById("quiz-section").style.display = "none";

})

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.1.0/firebase-app.js";
import { getDatabase, ref, onValue } from "https://www.gstatic.com/firebasejs/10.1.0/firebase-database.js";

const appSettings = {

    databaseURL: "https://questions-8316b-default-rtdb.europe-west1.firebasedatabase.app/",

}

const app = initializeApp(appSettings);
const database = getDatabase(app);
const quizQuestionsInDB = ref(database, "questions");
const question = document.getElementById("question-container");
const nextQuestionBtn = document.getElementById("next-question");
const questionNo = document.getElementById("question-number");

const answerOne = document.getElementById("answer-one");
const answerTwo = document.getElementById("answer-two");
const answerThree = document.getElementById("answer-three");
const answerFour = document.getElementById("answer-four");

const answerOptions = document.getElementsByClassName('answer-btn');
const quizResultsBox = document.getElementById("quiz-results-container");
const closeButton = document.getElementById("close-score-btn");
const scoreResult = document.getElementById("score-number");
const continueBtn = document.getElementById("continue-btn");

const closeBtnTwo = document.getElementById("close-saver-btn");
const saverResultsBox = document.getElementById("analysis-results-dialog");

closeButton.addEventListener("click", function(){
    quizResultsBox.close();
})

closeBtnTwo.addEventListener("click", function(){
    saverResultsBox.close();
    energySection.style.display = "block";
})


let r = 0;
let score = 0;
let c = 0;
let mixedRows;
let storedValues;
let q;
var qNumber = document.getElementById("q-number");

function initializeQuiz() {
    r = 0;
    c = 0;
    score = 0;
    questionNo.innerHTML = "Question " + (r + 1);
    nextQuestionBtn.innerHTML = "Next Question";
    mixedRows = mixingRowsInMatrix(storedValues);
    displayAnswers(mixedRows);
    quizResultsBox.close();
    for (let i = 0; i < answerOptions.length-1; i++) {

        if( r <= 9){
            answerOptions[i].style.backgroundColor = "rgb(238, 223, 223)";
            answerOptions[i].style.color = "rgb(66, 66, 66)";
            
        }
    }
    nextQuestionBtn.style.backgroundColor = "black";
    nextQuestionBtn.style.color = "white";
}

onValue(quizQuestionsInDB, function(quizQuestion){

    // q is an array containing all questions and answer from database
    q = Object.values(quizQuestion.val());

    storedValues = storingQuestionsAndAnswersInMatrix(q);

    mixedRows = mixingRowsInMatrix(storedValues);

    displayAnswers(mixedRows);

    nextQuestionBtn.addEventListener("click", function(){

        r++;
        for (let i = 0; i < answerOptions.length; i++) {

            if( r <= 9){
                answerOptions[i].style.backgroundColor = "rgb(238, 223, 223)";
                answerOptions[i].style.color = "rgb(66, 66, 66)";
                
            }
        }

        if( r === 9){
            nextQuestionBtn.innerHTML = "Finish Quiz";
            
        }

        nextQuestionBtn.style.backgroundColor = "black";
        nextQuestionBtn.style.color = "white";
        
        c = 0;
        displayAnswers(mixedRows);
        
    })

})


function storingQuestionsAndAnswersInMatrix( storeQ ){

    let matrix = [];
    let rows = 10;
    let cols = 6;
    let counter = 0;
    for (let i = 0; i < rows; i++) {
      matrix[i] = [];
      for (let j = 0; j < cols; j++) {
        matrix[i][j] = storeQ[counter];
        counter++;
      }
    }
    return matrix;

}

function mixingRowsInMatrix(mixingValues){

    let randNumOne;
    let randNumTwo;

    for(let i = 0; i < 100; i++){

        randNumOne = Math.floor( Math.random()*10);

        do{

            randNumTwo = Math.floor( Math.random()*10);

        }while(randNumTwo === randNumOne);

        let temp = mixingValues[randNumOne];
        mixingValues[randNumOne] = mixingValues[randNumTwo];
        mixingValues[randNumTwo] = temp;   

    }

    return mixingValues;
}

function displayAnswers(q){


    if( r > 9 ){
        quizResultsBox.showModal();
        scoreResult.innerHTML = "You got " + ((score/10)*100) + "% in the EirGrid Interactive Quiz!";
        questionNo.innerHTML = "Question " + (r);
    }

    if(r <= 9){
        questionNo.innerHTML = "Question " + (r+1);

        question.innerHTML = q[r][0];

        answerOne.innerHTML = q[r][1];
        answerTwo.innerHTML = q[r][2];
        answerThree.innerHTML = q[r][3];
        answerFour.innerHTML = q[r][4];

        qNumber.innerHTML = (r+1) + " out of 10";

        answerOne.addEventListener("click", function () {
            checkAnswer(answerOne, q[r][5]);
        });

        answerTwo.addEventListener("click", function () {
            checkAnswer(answerTwo, q[r][5]);
        });

        answerThree.addEventListener("click", function () {
            checkAnswer(answerThree, q[r][5]);
        });

        answerFour.addEventListener("click", function () {
            checkAnswer(answerFour, q[r][5]);
        });
    }
    
}

function checkAnswer(button, correctAnswer) {
    // Extract the letter and answer from the button's text content
    const selectedAnswer = button.innerHTML;

    // Check if the selected answer is equal to the correct answer
    if (selectedAnswer === correctAnswer) {
        // Change background color to green for correct answer
        button.style.backgroundColor = "rgb(30, 177, 30)";
        button.style.color = "white";
        if( c < 1){
            score++;
            c++;
        }
        
    } else {
        // Change background color to red for incorrect answer
        button.classList.add("wrong");
        button.style.backgroundColor = "rgb(255, 39, 39)";
        button.style.color = "white";
        c++;
    }

}

continueBtn.addEventListener("click", function(){

    document.getElementById("display-question").style.display = "none";
    document.getElementById("quiz-section").style.display = "block";
    initializeQuiz();
    
})


// Energy Saver Section
const startAnalysisBtn = document.getElementById("start-energy-analysis");
const energySteps = document.getElementById("display-analysis");


startAnalysisBtn.addEventListener("click", function(){
    energySection.style.display = "none";
    energySteps.style.display = "block";
})



document.addEventListener("DOMContentLoaded", function() {
    updateInputBoxes();

    // Add an onchange event listener to the select box
    document.getElementById("selectbox").addEventListener("change", updateInputBoxes);
});

let selectedRate = document.getElementById("selectbox").value;


function updateInputBoxes(){

    selectedRate = document.getElementById("selectbox").value;
    let oneInput = document.getElementById("rate-cost-1");
    let twoInputs = document.getElementById("rate-cost-2");
    let threeInputs = document.getElementById("rate-cost-3");
    let oneInput1 = document.getElementById("energy-rate-1");
    let twoInputs2 = document.getElementById("energy-rate-2");
    let threeInputs3 = document.getElementById("energy-rate-3");

    if(selectedRate == 2){
        oneInput.style.display = "none";
        twoInputs.style.display = "block";
        threeInputs.style.display = "none";
        oneInput1.style.display = "none";
        twoInputs2.style.display = "block";
        threeInputs3.style.display = "none";
    }

    else if(selectedRate == 3 ){
        oneInput.style.display = "none";
        twoInputs.style.display = "none";
        threeInputs.style.display = "block";
        oneInput1.style.display = "none";
        twoInputs2.style.display = "none";
        threeInputs3.style.display = "block";
    }

    else{
        oneInput.style.display = "block";
        twoInputs.style.display = "none";
        threeInputs.style.display = "none";
        oneInput1.style.display = "block";
        twoInputs2.style.display = "none";
        threeInputs3.style.display = "none";
    }

}

const energySaverResults = document.getElementById("analysis-results-dialog");
const finishEnergySaverBtn = document.querySelectorAll(".finish-btn");
const displayCost = document.getElementById("cost");
const displayEnergy = document.getElementById("energy");
const amountSaved = document.getElementById("savings")

for(let a = 0; a < finishEnergySaverBtn.length; a++){

    finishEnergySaverBtn[a].addEventListener("click", function(){

        energySaverResults.showModal();
        energySteps.style.display = "none";

        let costOfRate = [];
        let energyAtRate = [];

        if(selectedRate == 1){
            costOfRate.push(parseFloat(document.getElementById("rate-cost-1_1").value));
            energyAtRate.push(parseFloat(document.getElementById("energy-rate-1_1").value));
        }
        else if(selectedRate == 2){
            costOfRate.push(parseFloat(document.getElementById("rate-cost-2_1").value));
            energyAtRate.push(parseFloat(document.getElementById("energy-rate-2_1").value));
            costOfRate.push(parseFloat(document.getElementById("rate-cost-2_2").value));
            energyAtRate.push(parseFloat(document.getElementById("energy-rate-2_2").value));
        }
        else{
            costOfRate.push(parseFloat(document.getElementById("rate-cost-3_1").value));
            energyAtRate.push(parseFloat(document.getElementById("energy-rate-3_1").value));
            costOfRate.push(parseFloat(document.getElementById("rate-cost-3_2").value));
            energyAtRate.push(parseFloat(document.getElementById("energy-rate-3_2").value));
            costOfRate.push(parseFloat(document.getElementById("rate-cost-3_3").value));
            energyAtRate.push(parseFloat(document.getElementById("energy-rate-3_3").value));
        }

        let totalCost = 0;
        let totalEnergy = 0;
        let totalCostPercentage = 0;
        let saverTwo = 0;
        let saverThree = 0;

        for(let j = 0; j < costOfRate.length; j++){
            totalCost += ((costOfRate[j])/100)*energyAtRate[j]; 
        }
        for(let k = 0; k < energyAtRate.length; k++){
            totalEnergy += energyAtRate[k]; 
        }

        totalCostPercentage = (totalCost*0.1).toFixed(2);
        if(selectedRate == 1){
            amountSaved.innerHTML = "You could save €" + totalCostPercentage + " by reducing your consumption by 10%";
        }
        else if(selectedRate == 2){
            saverTwo = (totalCostPercentage/costOfRate[1]);
            amountSaved.innerHTML = "You could save €" + saverTwo.toFixed(2) + " by shifting 10% of your consumption to off-peak hours";
        }
        else if(selectedRate == 3){
            saverThree = (totalCostPercentage/costOfRate[2]);
            amountSaved.innerHTML = "You could save €" + saverThree.toFixed(2) + " by shifting 10% of your consumption to off-peak hours";
        }

        displayCost.innerHTML = "Your total energy bill is: €" + totalCost.toFixed(2);
        displayEnergy.innerHTML = "You consumed " + totalEnergy.toFixed(2) + " kW of energy";
    })
}

const continueBtnTwo = document.getElementById("continue-btn-2");

continueBtnTwo.addEventListener("click", function(){

    document.getElementById("energy-section").style.display = "block";
    saverResultsBox.close();
})



