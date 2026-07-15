import * as fs from 'fs';

const pets: { [key: string]: { colors: string[]; states: string[] } } = {
    kris: {
        colors: ['darkworld'],
        states: ['idle', 'run', 'swipe', 'walk', 'walk_fast', 'with_ball'],
    },
    lancer: {
        colors: ['darkworld'],
        states: ['idle', 'run', 'swipe', 'walk', 'walk_fast', 'with_ball'],
    },
    ralsei: {
        colors: ['darkworld'],
        states: ['idle', 'run', 'swipe', 'walk', 'walk_fast', 'with_ball'],
    },
    noelle: {
        colors: ['darkworld'],
        states: ['idle', 'run', 'swipe', 'walk', 'walk_fast', 'with_ball'],
    },
    susie: {
        colors: ['darkworld'],
        states: ['idle', 'run', 'swipe', 'walk', 'walk_fast', 'with_ball'],
    },
    spamton: {
        colors: ['darkworld'],
        states: ['idle', 'run', 'swipe', 'walk', 'walk_fast', 'with_ball'],
    },
    jevil: {
        colors: ['darkworld'],
        states: ['idle', 'run', 'swipe', 'walk', 'walk_fast', 'with_ball'],
    },
    tenna: {
        colors: ['darkworld'],
        states: ['idle', 'run', 'swipe', 'walk', 'walk_fast', 'with_ball'],
    },
};

function checkGifFilenames(folder: string) {
    for (const pet in pets) {
        const allowedColors = pets[pet].colors;
        const allowedStates = pets[pet].states;
        if (!allowedColors) {
            console.error(`No colors found for pet "${pet}"`);
            return;
        }
        allowedColors.forEach((color) => {
            allowedStates.forEach((state) => {
                const filename = `${color}_${state}_8fps.gif`;
                const filePath = `${folder}/${pet}/${filename}`;
                if (!fs.existsSync(filePath)) {
                    // \x1b[31m is the ANSI escape code for red, and \x1b[0m resets the color back to the terminal's default.
                    console.error(
                        `\x1b[31mFile "${filePath}" does not exist.\x1b[0m`,
                    );
                    return false;
                } else {
                    // console.log(`File "${filePath}" exists.`);
                }
            });

            // Check icon as well
            const iconFilename = `icon_${color}.png`;
            const iconFilePath = `${folder}/${pet}/${iconFilename}`;
            if (!fs.existsSync(iconFilePath)) {
                if (fs.existsSync(`${folder}/${pet}/icon.png`)) {
                    console.warn(
                        `\x1b[33mNo icon found for "${pet}" with color "${color}". Using default icon.\x1b[0m`,
                    );
                } else {
                    console.error(
                        `\x1b[31mFile "${iconFilePath}" and "${folder}/${pet}/icon.png" does not exist.\x1b[0m`,
                    );
                }
                return false;
            } else {
                // console.log(`File "${iconFilePath}" exists.`);
            }
        });
    }
}

const mediaFolder = './media';
checkGifFilenames(mediaFolder);
