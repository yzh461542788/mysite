/**
 * Created by zihao on 2017/1/8.
 */
function calculate() {
    let msg = document.getElementById("message");
    msg.innerHTML = "计算中...请稍等";
    let rates = Array.from(document.getElementsByClassName('rate')).map(x => x.value);
    let iteration = document.getElementById("iterations").value;
    if (!isNumeric(iteration) || iteration <= 0) {
        msg.innerHTML = "请输入正确的模拟次数";
        return;
    }
    let deck = [
        Array.from(document.getElementsByClassName('a-deck')).map(x => x.value),
        Array.from(document.getElementsByClassName('b-deck')).map(x => x.value)
    ];
    if (document.getElementById('4ban1').checked) {
        rates = [
            rates.slice(0, 4),
            rates.slice(5, 9),
            rates.slice(10, 14),
            rates.slice(15, 19),
        ];
    } else {
        rates = [
            rates.slice(0, 5),
            rates.slice(5, 10),
            rates.slice(10, 15),
            rates.slice(15, 20),
            rates.slice(20, 25),
        ];
    }
    for (let rate of rates) {
        for (r of rate) {
            if (!isNumeric(r) || r < 0 || r > 1) {
                msg.innerText = "输入有误，请输入正确的胜率（0.0～1.0）";
                return;
            }
        }
    }

    let result = [];
    for (let i = 0; i < rates.length; i++) {
        let row = [];
        for (let j = 0; j < rates.length; j++) {
            let newRates = rates.map(row => row.slice());
            newRates.splice(i, 1);
            newRates.forEach(row => row.splice(j, 1));
            let r = getRate(newRates, iteration);
            row.push(r);
        }
        result.push(row);
    }
    let sum = [new Array(rates.length).fill(0), new Array(rates.length).fill(0)];
    for (let i = 0; i < rates.length; i++) {
        for (let j = 0; j < rates.length; j++) {
            sum[0][i] += result[i][j];
            sum[1][j] += result[i][j];
        }
    }

    let message = "<table><caption>BAN选后总体胜率估计:</caption><thead><tr><th>你被BAN的卡组\\对手被BAN的卡组</th>";
    for (let i = 0; i < rates.length; i++) {
        message += "<th>" + deck[1][i] + "</th>";
    }
    message += "<th>平均</th></tr></thead><tbody>";
    for (let i = 0; i < rates.length; i++) {
        message += "<tr>";
        message += ("<th>" + deck[0][i] + "</th>");
        result[i].forEach(x => message += ("<td>" + x + "</td>"));
        message += "<td>" + (sum[0][i] / rates.length).toFixed(4) + "</td></tr>";
    }
    message += "<tr><th>平均</th>";
    let avg = [];
    for (let i = 0; i < rates.length; i++) {
        avg[i] = sum[1][i] / rates.length;
        message += ("<td>" + avg[i].toFixed(4) + "</td>");
    }
    message += ("<td>" + (avg.reduce((a, b) => a + b)/ rates.length).toFixed(4) + "</td>");

    message += "</tr></tbody></table>";
    msg.innerHTML = message;
}

function isNumeric(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}

function checkState() {
    if (document.getElementById('4ban1').checked) {
        Array.from(document.getElementsByClassName('optional')).forEach(x => x.style.display = 'none');
    } else {
        Array.from(document.getElementsByClassName('optional')).forEach(x => x.style.display = '');
    }
}

function getRate(rateMatrix, iteration) {
    let win = [0, 0];
    for (let i = 0; i < iteration; i++) {
        let remain = [
            Array.from(new Array(rateMatrix.length).keys()),
            Array.from(new Array(rateMatrix.length).keys())
        ];
        while (true) {
            let choice = [
                remain[0][Math.floor(Math.random() * remain[0].length)],
                remain[1][Math.floor(Math.random() * remain[1].length)]];
            if (Math.random() < rateMatrix[choice[0]][choice[1]]) {
                remain[0].splice(remain[0].indexOf(choice[0]), 1);
            } else {
                remain[1].splice(remain[1].indexOf(choice[1]), 1);
            }
            if (remain[0].length === 0) {
                win[0] += 1;
                break;
            }
            if (remain[1].length === 0) {
                win[1] += 1;
                break;
            }
        }
    }
    return win[0] / iteration;
}
