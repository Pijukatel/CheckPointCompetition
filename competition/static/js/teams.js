async function scoreBoardUpdate() {
    document.getElementById("scoreBoard")
    const scores =  await requestScore();
    const scoreBoard = document.getElementById("scoreBoard");
    const rows = scoreBoard.children;
    const missingNodes= scores.length - rows.length
    if (missingNodes > 0) {
        for (let i = missingNodes; i>0; i--){
            scoreBoard.appendChild(rows[0].cloneNode(true));
        }
    }

    scores.forEach((score,index)=>{
        const columns = rows[index].children
        columns[0].innerHTML = `<a href="/team/${score.team}/"> ${score.team} </a>`
        columns[1].innerHTML = score.points
        columns[2].innerHTML = score.latest_updated_point
    })

}

setInterval(scoreBoardUpdate, 5000)


