"use strict";
function journal_config() {
    return {
        journalDir: "01-journal",
        types: {
            daily: "journal/daily",
            weekly: "journal/weekly",
            monthly: "journal/monthly",
            yearly: "journal/yearly",
        },
        tags: {
            daily: ["journal", "journal/daily"],
            weekly: ["journal", "journal/weekly"],
            monthly: ["journal", "journal/monthly"],
            yearly: ["journal", "journal/yearly"],
        },
        weekStart: "isoWeek",
        days: ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
    };
}
module.exports = journal_config;
