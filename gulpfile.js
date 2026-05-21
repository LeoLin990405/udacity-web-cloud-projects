import { spawn } from "node:child_process";
import gulp from "gulp";

const runCommand = (command, args) => {
  return (done) => {
    const child = spawn(command, args, {
      stdio: "inherit",
    });

    child.on("close", (code) => {
      if (code === 0) {
        done();
        return;
      }

      done(new Error(`${command} ${args.join(" ")} exited with code ${code}`));
    });
  };
};

export const lint = runCommand("npx", [
  "eslint",
  "src/utilityRenderFunctions.js",
  "src/shuffle.js",
]);
export const build = runCommand("npx", ["parcel", "build", "index.html"]);
export const serve = runCommand("npx", [
  "parcel",
  "index.html",
  "--host",
  "127.0.0.1",
]);
export const unitTest = runCommand("npx", ["mocha", "test/**/*.js"]);
export const cypress = runCommand("npm", ["run", "cypress:run"]);

export const test = gulp.series(unitTest);
export const verify = gulp.series(lint, unitTest, build, cypress);

export default verify;
