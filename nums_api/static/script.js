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

/**
 * On submission of search form performs search of
 * facts in sandbox, displaying the fact on page.
 */
$("#search-form").on("submit", async function () {

    const text = $("#search-text").text();
    const fact = await getFacts(text);

    const number = text.replace(/\D/g, "");


    $("#result-temporary-text").text(fact);
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



$("#add-number").on("click", () => {updateCounter(1,"add")});



function updateCounter(num,action="replace"){
    const currentTick = $(".tick").data("value");
    let numTick = parseInt(currentTick);


    if(action === "add"){
        let newNum = (numTick + num).toString();
        $(".tick").attr("data-value",newNum);
    } else if (action === "subtract" && currentTick !== "0000"){
        let newNum = toString(numTick - num);
        $(".tick").attr("data-value",newNum);
    } else if (action === "replace"){
        $(".tick").attr("data-value",num.toString());
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

    return resp.data.fact.statement;
}


// function handleTickInit(tick) {

//     Tick.helper.interval(function() {

//         tick.value++;

//         // The aria-label attribute is
//         // used instead of the actual
//         // tick content
//         tick.root.setAttribute(
//             'aria-label',
//             tick.value
//         );

//     }, 1000);

// }



