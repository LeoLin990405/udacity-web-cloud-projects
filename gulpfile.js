import gulp from "gulp";
import shell from "gulp-shell";

export const build = shell.task(["npx parcel build index.html"]);
export const serve = shell.task(["npx parcel index.html --host 127.0.0.1"]);
export const test = shell.task(["npx mocha \"test/**/*.js\""]);
export const cypress = shell.task(["npx cypress run"]);

export default gulp.series(build, serve);
