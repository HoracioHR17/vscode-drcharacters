import { PetColor } from '../../common/types';
import { BasePetType } from '../basepettype';
import { States } from '../states';

abstract class DeltarunePet extends BasePetType {
    static possibleColors = [PetColor.darkworld];
    sequence = {
        startingState: States.sitIdle,
        sequenceStates: [
            {
                state: States.sitIdle,
                possibleNextStates: [States.walkRight, States.runRight],
            },
            {
                state: States.walkRight,
                possibleNextStates: [States.walkLeft, States.runLeft],
            },
            {
                state: States.runRight,
                possibleNextStates: [States.walkLeft, States.runLeft],
            },
            {
                state: States.walkLeft,
                possibleNextStates: [States.sitIdle, States.runRight],
            },
            {
                state: States.runLeft,
                possibleNextStates: [States.sitIdle, States.walkRight],
            },
            {
                state: States.chase,
                possibleNextStates: [States.idleWithBall],
            },
            {
                state: States.idleWithBall,
                possibleNextStates: [States.walkRight, States.walkLeft],
            },
        ],
    };
}

export class Kris extends DeltarunePet {
    label = 'kris';
    static possibleColors = [PetColor.darkworld];
    get emoji() {
        return '💙';
    }
    get hello() {
        return `The power of fluffy boys shines within you.`;
    }
}

export class Lancer extends DeltarunePet {
    label = 'lancer';
    static possibleColors = [PetColor.darkworld];
    get emoji() {
        return '♠️';
    }
    get hello() {
        return `Ho ho ho! The bad guy is here!`;
    }
}

export class Ralsei extends DeltarunePet {
    label = 'ralsei';
    static possibleColors = [PetColor.darkworld];
    get emoji() {
        return '🧣';
    }
    get hello() {
        return `I'm the prince of this kingdom...`;
    }
}

export class Noelle extends DeltarunePet {
    label = 'noelle';
    static possibleColors = [PetColor.darkworld];
    get emoji() {
        return '🦌';
    }
    get hello() {
        return `Let's make a nice team!`;
    }
}

export class Susie extends DeltarunePet {
    label = 'susie';
    static possibleColors = [PetColor.darkworld];
    get emoji() {
        return '🪓';
    }
    get hello() {
        return `Let's just get this over with.`;
    }
}

export class Spamton extends DeltarunePet {
    label = 'spamton';
    static possibleColors = [PetColor.darkworld];
    get emoji() {
        return '📞';
    }
    get hello() {
        return `NOW'S YOUR CHANCE TO BE A BIG SHOT!`;
    }
}

export class Jevil extends DeltarunePet {
    label = 'jevil';
    static possibleColors = [PetColor.darkworld];
    get emoji() {
        return '🃏';
    }
    get hello() {
        return `CHAOS, CHAOS! I CAN DO ANYTHING!`;
    }
}

export class Tenna extends DeltarunePet {
    label = 'tenna';
    static possibleColors = [PetColor.darkworld];
    get emoji() {
        return '📺';
    }
    get hello() {
        return `Welcome, my friends, to the greatest show!`;
    }
}

export const KRIS_NAMES: ReadonlyArray<string> = ['Kris'];
export const LANCER_NAMES: ReadonlyArray<string> = ['Lancer'];
export const RALSEI_NAMES: ReadonlyArray<string> = ['Ralsei'];
export const NOELLE_NAMES: ReadonlyArray<string> = ['Noelle'];
export const SUSIE_NAMES: ReadonlyArray<string> = ['Susie'];
export const SPAMTON_NAMES: ReadonlyArray<string> = ['Spamton G. Spamton'];
export const JEVIL_NAMES: ReadonlyArray<string> = ['Jevil'];
export const TENNA_NAMES: ReadonlyArray<string> = ['Mr. "Ant" Tenna'];
