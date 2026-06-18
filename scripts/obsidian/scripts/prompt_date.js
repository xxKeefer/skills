"use strict";
async function prompt_date(tp, prompt = "Enter any date") {
    const now = tp.date.now("YYYY-MM-DD");
    const msg = `${prompt} (e.g., ${now})`;
    const date = await tp.system.prompt(msg, now);
    return moment(date);
}
module.exports = prompt_date;
