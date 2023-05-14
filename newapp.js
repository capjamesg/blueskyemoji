const express = require("express");
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

function getMostRecentFileName(dir) {
    var files = fs.readdirSync(dir);

    return _.max(files, function (f) {
        var fullpath = path.join(dir, f);

        return fs.statSync(fullpath).ctime;
    });
}

app.route("/").get(async (req, res) => {
    // load most recent file
    return res.render("index", {});
});

// run in production mode
app.listen(PORT, () => {
    console.log("Server started on port " + PORT);
});