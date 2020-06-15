const { app, BrowserWindow, Menu, dialog, ipcMain } = require("electron");
// const { spawn } = require("child_process");
const { PythonShell } = require("python-shell");
const path = require("path");
const fs = require("fs");

let mainWindow;

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require("electron-squirrel-startup")) {
  // eslint-disable-line global-require
  app.quit();
}

const createWindow = () => {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 600,
    height: 300,
    webPreferences: {
      nodeIntegration: true,
    },
    icon: '/home/chris/Documents/mylogo/ttlogo.png'
  });

  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, "index.html"));

  // Open the DevTools.
  mainWindow.webContents.openDevTools();
  console.log(app.getAppPath())
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on("ready", createWindow);

// Quit when all windows are closed.
app.on("window-all-closed", () => {
  // On OS X it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  // On OS X it"s common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// In this file you can include the rest of your app"s specific main process
// code. You can also put them in separate files and import them here.

var menu = Menu.buildFromTemplate([
  {
    options: {
      filters: [
        { name: "Images", extensions: ["jpg", "png", "jpeg"] }
      ],
    },
    label: "File",
    submenu: [
      {
        label: "Open File...",
        click: function click() {
          openFile();
        },

        accelerator: "CmdOrCtrl+O",
      },
      {
        label: "Save Schem",
        click: function click() {
          saveFile();
        },

        accelerator: "CmdOrCtrl+S",
      },
      {
        label: "Exit",
        click: function click() {
          app.quit();
        },

        accelerator: "CmdOrCtrl+Q",
      },
    ],
  },
]);

Menu.setApplicationMenu(menu);

async function openFile() {
  var files = await dialog.showOpenDialog(mainWindow, {
    properties: ["openFile"],
    filters: [
      { name: "Image", extensions: ["jpg", "png", "jpeg"] }
    ],
  });
  if (!files) return;
  mainWindow.webContents.send("upload", files.filePaths[0]);
}

async function saveFile() {
  var save = await dialog.showSaveDialog(mainWindow, {
    properties: ["showOverwriteConfirmation"],
    filters: [
      { name: "Schematic", extensions: ["schem"] }
    ],
  });
  fs.rename(app.getAppPath() + "/temp/upload1.schem", save.filePath, function (err) {
    if (err) throw err;
  })
}

ipcMain.on("async-message", (event, arg) => {
  var options = {
    args: [arg, app.getAppPath()]
  }
  PythonShell.run(app.getAppPath() + "/py/main.py", options, function (err, results) {
    if (err) throw err;
    console.log(results);
    event.reply("async-reply", results)
  })
});


