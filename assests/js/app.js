const states = ["Closed", "Open"];

let nlogs = 0;

function fetchData() {
    fetch('/test')
        .then(response => response.json())
        .then(data => {
            Object.keys(data).forEach(key => {
                if (data[key] === 1) {
                    document.getElementById(key).classList.add("Open");
                } else {
                    document.getElementById(key).classList.remove("Open");
                }
                // console.log(key, states[data[key]]);
            });
            console.log("Done!!");
            // setTimeout(fetchData, 1000); 
        })
}

function fetchLogs(){
    fetch('/doorlogs')
        .then(response => response.json())
        .then(data => {
            if (data.logs.length != nlogs) {
                let table = document.getElementById("door-logs");
                table.innerHTML = "";
                const new_tbody = document.createElement('tbody');
                data.logs.forEach(log => {
                    const arr = log.split(',');
                    const row = document.createElement("tr");
                    arr.forEach(element => {
                        const c = document.createElement("td");
                        const p = document.createElement("p");
                        p.innerText = element;
                        c.appendChild(p);
                        row.appendChild(c);
                    })
                    
                    // const c1 = document.createElement("td");
                    // const c2 = document.createElement("td");
                    
                    // const p1 = document.createElement("p");
                    // const p2 = document.createElement("p");
                    
                    // p2.innerText = arr[1];
                    
                    // c1.appendChild(p1);
                    // c2.appendChild(p2);
                    // row.appendChild(c1);
                    // row.appendChild(c2);
                    table.prepend(row)
                })
                nlogs = data.logs.length;
                // table.parentNode.replaceChild(newTable, table);
                console.log("changed");
            }
        })
    }
    
fetchLogs();
// fetchData();
setInterval(fetchLogs, 1000);
setInterval(fetchData, 1000);