const oneQs=document.getElementById("question1");
const twoQs=document.getElementById("question2");
const threeQs=document.getElementById("question3");
const fourQs=document.getElementById("question4");
const oneAns=document.getElementById("answer1");
const twoAns=document.getElementById("answer2");
const threeAns=document.getElementById("answer3");
const fourAns=document.getElementById("answer4");

oneQs.addEventListener("click", () =>{
    oneAns.classList.toggle("hide");

    if(oneQs.src.endsWith("icon-plus.svg")){
        oneQs.src="assets/images/icon-minus.svg"
    }else{
        assets/images/icon-minus.svg
    }
});

twoQs.addEventListener("click", () =>{
    twoAns.classList.toggle("hide");

    if(twoQs.src.endswith("icon-plus.svg")){
        twoQs.src="assets/images/icon-minus.svg"
    }else{
        assets/images/icon-minus.svg
    }
});

threeQs.addEventListener("click", () =>{
    threeAns.classList.toggle("hide");

    if(threeQs.src.endswith("icon-plus.svg")){
        threeQs.src="assets/images/icon-minus.svg"
    }else{
        assets/images/icon-minus.svg
    }
});

fourQs.addEventListener("click", () =>{
    fourAns.classList.toggle("hide");

    if(fourQs.src.endswith("icon-plus.svg")){
        fourQs.src="assets/images/icon-minus.svg"
    }else{
        assets/images/icon-minus.svg
    }
});
