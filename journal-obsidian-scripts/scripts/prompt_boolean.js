"use strict";
async function prompt_boolean(tp, prompt, defaultResponse) {
    const response = await tp.system.prompt(prompt, defaultResponse);
    if (response === null)
        return false;
    return ["yes", "y", "true", "1"].includes(response.toLowerCase());
}
module.exports = prompt_boolean;
