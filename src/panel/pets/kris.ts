import { PetColor } from '../../common/types';
import { BasePetType } from '../basepettype';
import { States } from '../states';

export class Kris extends BasePetType {
    label = 'kris';
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

    get emoji(): string {
        return '💙';
    }

    get hello(): string {
        return `The power of fluffy boys shines within you.`;
    }
}

export const KRIS_NAMES: ReadonlyArray<string> = ['Kris'];
