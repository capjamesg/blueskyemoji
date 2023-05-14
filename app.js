const express = require("express");
const ejs = require("ejs");
const fs = require("fs");

const app = express();

app.set("view engine", "ejs");
app.use(express.static("public"));
app.use((err, req, res, next) => {
    res.status(500).render("error", {
        error: "There was an error loading this page."
    });
});

const PORT = 3002;

app.route("/").get(async (req, res) => {
    const files = fs.readdirSync("data/");
    // open file edited most recently
    const mostRecentFile = files.sort((a, b) => {
        return fs.statSync("data/" + a).mtime.getTime() - fs.statSync("data/" + b).mtime.getTime();
    }).reverse()[0];
    const data = JSON.parse(fs.readFileSync("data/" + mostRecentFile, "utf8"));

    return res.render("index", {
        emojis: data
    });
});

// run in production mode
app.listen(PORT, () => {
    console.log("Server started on port " + PORT);
});