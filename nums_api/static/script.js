"use strict";

const BASE_URL = "http://localhost:5001/api/";

/**
 * Listens for click on data type cards and performs a
 *  fact search in Sandbox.
 */
$(".example-box-address").on("click", async function (evt) {
    const numAddress = $(evt.target).text();

    const shortAddress = numAddress.replace("numbersapi.com/api/", "");

    $("#search-text").val(shortAddress);
    $("#search-form").submit();

});

$("#search-link").on("click", function (evt) {
    const searchText = $("#search-text").val();
    
    const urlToVisit = `${BASE_URL}${searchText}`;
    
    window.location.href = urlToVisit;
})

/** Async function for replacing result-temporary-text box with text based
 * on URL text given, and updates counter.
 */
async function updateResultTextAndCounter() {
    const text = $("#search-text").val();
    const respData = await getFacts(text);

    if (respData.error) {
        $("#result-temporary-text").text(respData.error.message);
        return;
    }

    if (!respData.fact.number) {
        updateCounter(respData.fact.year);
    } else {
        updateCounter(respData.fact.number);
    }

    $("#result-temporary-text").text(respData.fact.statement);
}

/**
 * On submission of search form performs search of
 * facts in sandbox, displaying the fact on page and updating counter.
 */
$("#search-form").on("submit", async function (evt) {
    evt.preventDefault();
    // Shouldn't need the logic below, setting the number
    //should be handled correctly in getFacts

    // const text = $("#search-text").val();

    // if (!text.includes("random")) {

    //     const urlNum = text.replace(/(trivia|years|math)\//g, "");
    //     updateCounter(urlNum);
    // }
    updateResultTextAndCounter();
});


/**
 * When clicking datatype for random, performs
 * a random search of that data type in the sandbox.
 */
$(".random-fact").on("click", function (evt) {

    const text = $(evt.target).text();
    $("#search-text").val(text);
    $("#search-form").submit();
});

/** Clicking the "+" button will update counter and fact */
$("#add-number").on("click", async function () {
    const currentTick = $(".tick").attr("data-value");
    const numTick = parseInt(currentTick);

    const newNum = (numTick + 1).toString();

    const text = $("#search-text").val();
    if (text.includes("date")) {
        updateSandboxForDates(text, newNum);
    }

    else {
        if (text.includes("random")) {
            const newText = text.replace("random", newNum);
            $("#search-text").val(newText);
        }
        else {
            const newText = text.replace(/\d/g, "").concat(newNum);
            $("#search-text").val(newText);
        }
    }

    updateResultTextAndCounter();
});

/** Clicking the "-" button will update counter and fact */
$("#subtract-number").on("click", async function () {
    const currentTick = $(".tick").attr("data-value");
    const numTick = parseInt(currentTick);

    if (numTick <= 0) return;

    const newNum = (numTick - 1).toString();

    const text = $("#search-text").val();
    if (text.includes("date")) {
        updateSandboxForDates(text, newNum);
    }

    else {
        const newText = text.replace(/\d/g, "").concat(newNum);
        $("#search-text").val(newText);
    }

    updateResultTextAndCounter();
});

/** Converts date of year to month and day and uses it to update search text URL */
function updateSandboxForDates(text, dateOfYear) {
    const date = new Date(2004, 0, dateOfYear);

    const day = date.getDate();
    const month = date.getMonth() + 1;

    const MonthAndDay = `${month}/${day}`;

    let newText;

    if (text.includes("random")) {
        newText = text.replace("random", MonthAndDay);
    } else {
        newText = text.replace(/(\d+)\/(\d+)/g, MonthAndDay);
    };

    $("#search-text").val(newText);
}

/** Updates counter and updates text in result text box */
async function updateCounter(num) {

    const paddedNum = String(num).padStart(4, "0");
    $(".tick").attr("data-value", paddedNum);
    return;

}

/**
 * Takes a partial URL or full URL address stringfor API
 * "math/5" or "localhost:5001/api/math/5"
 * returns a fact Statement string
 */

async function getFacts(address) {
    // if (address.includes("api")) {
    //     resp = await axios.get(address);
    // } else {
    //     resp = await axios.get(BASE_URL + address);
    // }
    const resp = await axios.get(BASE_URL + address);

    return resp.data;
}
