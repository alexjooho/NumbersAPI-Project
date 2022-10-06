const BASE_URL = "numbersapi.com/api/";

/**
 * Listens for click on data type cards and performs a
 *  fact search in Sandbox.
 */
$(".example-box-address").on("click", async function (evt) {
    let numAddress = $(evt.target).text();
    let shortAddress = numAddress.replace("numbersapi.com/api/", "");

    $("search-text").text(shortAddress);
    $("search-form").submit();

});

/** Async function for replacing result-temporary-text box with text based
 * on URL text given.
 */
async function updateResultText() {
    const text = $("#search-text").text();
    const fact = await getFacts(text);

    $("#result-temporary-text").text(fact);
}

/**
 * On submission of search form performs search of
 * facts in sandbox, displaying the fact on page and updating counter.
 */
$("#search-form").on("submit", async function (evt) {
    evt.preventDefault();

    const urlNum = $("#search-text").text().replace(/\D/g, "");

    updateCounter(urlNum);
    updateResultText();
});


/**
 * When clicking datatype for random, performs
 * a random search of that data type in the sandbox.
 */
$(".random-fact").on("click", function (evt) {
    let text = $(evt.target).text();

    $("search-text").text(text);
    $("search-form").submit();
});


$("#add-number").on("click", async function () { updateCounter(1, "add"); });
$("#subtract-number").on("click", async function () { updateCounter(1, "subtract"); });

/** Converts date of year to month and day and uses it to update search text URL */
function updateSandboxForDates(text, dateOfYear) {
    const date = new Date(2004, 0, dateOfYear);

    const day = date.getDate();
    const month = date.getMonth();

    const MonthAndDay = `${month}/${day}`;

    let newText;

    if (text.includes("random")) {
        newText = text.replace("random", MonthAndDay);
    } else {
        newText = text.replace(/(\d+)\/(\d+)/g, MonthAndDay);
    };

    $("#search-text").text(newText);
}

/** Updates counter and updates text in result text box */
async function updateCounter(num, action = "replace") {

    const currentTick = $(".tick").attr("data-value");
    let numTick = parseInt(currentTick);

    let newNum;

    if (action === "add") {
        newNum = (numTick + num).toString();

        if (newNum.length < 4) newNum = String(newNum).padStart(4, "0");

        $(".tick").attr("data-value", newNum);

    } else if (action === "subtract" && currentTick !== "0000") {
        newNum = (numTick - num).toString();
        if (newNum.length < 4) newNum = String(newNum).padStart(4, "0");

        $(".tick").attr("data-value", newNum);

    } else if (action === "replace") {
        newNum = String(num).padStart(4, "0");
        $(".tick").attr("data-value", newNum);
        return;
    }

    const text = $("#search-text").text();
    if (text.includes("date")) {
        updateSandboxForDates(text, newNum);
        updateResultText();
    }


    else {
        let newText = text.replace(/\d/g, "").concat(newNum);
        newText = newText.replace(/^0+/, "");
        $("#search-text").text(newText);
        updateResultText();
    }
}

/**
 * Takes a partial URL or full URL address stringfor API
 * "math/5" or "numbersapi.com/api/math/5"
 * returns a fact Statement string
 */

async function getFacts(address) {
    let resp;

    if (address.includes("api")) {
        resp = await axios.get(address);
    } else {
        resp = await axios.get(BASE_URL + address);
    }

    if (resp.error) return resp.error.message;

    if (!resp.data.fact.number) {
        updateCounter(resp.data.fact.year);
    } else {
        updateCounter(resp.data.fact.number);
    }

    return resp.data.fact.statement;
}


// function handleTickInit(tick) {

//     Tick.helper.interval(function() {

//         tick.value++;

//         // The aria-label attribute is
//         // used instead of the actual
//         // tick content
//         tick.root.setAttribute(
//             "aria-label",
//             tick.value
//         );

//     }, 1000);

// }