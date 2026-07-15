import { PetColor, PetSize, PetSpeed, PetType } from '../common/types';
import {
    Jevil,
    Kris,
    Lancer,
    Noelle,
    Ralsei,
    Spamton,
    Susie,
    Tenna,
} from './pets/deltarune';
import { IPetType } from './states';

export class PetElement {
    el: HTMLImageElement;
    collision: HTMLDivElement;
    speech: HTMLDivElement;
    pet: IPetType;
    color: PetColor;
    type: PetType;
    remove() {
        this.el.remove();
        this.collision.remove();
        this.speech.remove();
        this.color = PetColor.null;
        this.type = PetType.null;
        this.pet.remove();
    }

    constructor(
        el: HTMLImageElement,
        collision: HTMLDivElement,
        speech: HTMLDivElement,
        pet: IPetType,
        color: PetColor,
        type: PetType,
    ) {
        this.el = el;
        this.collision = collision;
        this.speech = speech;
        this.pet = pet;
        this.color = color;
        this.type = type;
    }
}

export interface IPetCollection {
    pets: Array<PetElement>;
    push(pet: PetElement): void;
    reset(): void;
    seekNewFriends(): void;
    locate(name: string): PetElement | undefined;
    locatePet(
        name: string,
        type: string,
        color: string,
    ): PetElement | undefined;
    remove(pet: PetElement): void;
}

export class PetCollection implements IPetCollection {
    private _pets: Array<PetElement>;

    constructor() {
        this._pets = new Array(0);
    }

    public get pets() {
        return this._pets;
    }

    push(pet: PetElement) {
        this._pets.push(pet);
    }

    reset() {
        this._pets.forEach((pet) => {
            pet.remove();
        });
        this._pets = [];
    }

    locate(name: string): PetElement | undefined {
        return this._pets.find((collection) => {
            return collection.pet.name === name;
        });
    }

    locatePet(
        name: string,
        type: string,
        color: string,
    ): PetElement | undefined {
        return this._pets.find((collection) => {
            return (
                collection.pet.name === name &&
                collection.type === type &&
                collection.color === color
            );
        });
    }

    remove(targetPet: PetElement): any {
        this._pets.forEach((pet) => {
            if (pet === targetPet) {
                pet.remove();
            }
        });
        this._pets = this._pets.filter((pet) => {
            return pet !== targetPet;
        });
    }

    seekNewFriends(): void {
        if (this._pets.length <= 1) {
            return;
        } // You can't be friends with yourself.
        const theFriendless = this._pets.filter((pet) => !pet.pet.hasFriend);
        if (theFriendless.length <= 1) {
            return;
        } // Nobody to be friends with.
        theFriendless.forEach((lonelyPet) => {
            const potentialFriends = theFriendless.filter(
                (pet) => pet !== lonelyPet,
            ); // Exclude the lonely pet itself.
            potentialFriends.forEach((potentialFriend) => {
                if (!potentialFriend.pet.canChase) {
                    return;
                } // Pet is busy doing something else.
                if (
                    potentialFriend.pet.left > lonelyPet.pet.left &&
                    potentialFriend.pet.left <
                        lonelyPet.pet.left + lonelyPet.pet.width
                ) {
                    // We found a possible new friend..
                    console.log(
                        lonelyPet.pet.name,
                        ' wants to be friends with ',
                        potentialFriend.pet.name,
                        '.',
                    );
                    if (lonelyPet.pet.makeFriendsWith(potentialFriend.pet)) {
                        potentialFriend.pet.showSpeechBubble('❤️', 2000);
                        lonelyPet.pet.showSpeechBubble('❤️', 2000);
                    }
                }
            });
        });
    }
}

export class InvalidPetException {
    message?: string;

    constructor(message?: string) {
        this.message = message;
    }
}

export function createPet(
    petType: string,
    el: HTMLImageElement,
    collision: HTMLDivElement,
    speech: HTMLDivElement,
    size: PetSize,
    left: number,
    bottom: number,
    petRoot: string,
    floor: number,
    name: string,
): IPetType {
    if (name === undefined || name === null || name === '') {
        throw new InvalidPetException('name is undefined');
    }

    const standardPetArguments: [
        HTMLImageElement,
        HTMLDivElement,
        HTMLDivElement,
        PetSize,
        number,
        number,
        string,
        number,
        string,
    ] = [el, collision, speech, size, left, bottom, petRoot, floor, name];

    switch (petType) {
        case PetType.kris:
            return new Kris(...standardPetArguments, PetSpeed.normal);
        case PetType.lancer:
            return new Lancer(...standardPetArguments, PetSpeed.fast);
        case PetType.ralsei:
            return new Ralsei(...standardPetArguments, PetSpeed.normal);
        case PetType.noelle:
            return new Noelle(...standardPetArguments, PetSpeed.normal);
        case PetType.susie:
            return new Susie(...standardPetArguments, PetSpeed.fast);
        case PetType.spamton:
            return new Spamton(...standardPetArguments, PetSpeed.veryFast);
        case PetType.jevil:
            return new Jevil(...standardPetArguments, PetSpeed.veryFast);
        case PetType.tenna:
            return new Tenna(...standardPetArguments, PetSpeed.fast, 2);
        default:
            throw new InvalidPetException("Pet type doesn't exist");
    }
}

export function availableColors(petType: PetType): PetColor[] {
    switch (petType) {
        case PetType.kris:
            return Kris.possibleColors;
        case PetType.lancer:
            return Lancer.possibleColors;
        case PetType.ralsei:
            return Ralsei.possibleColors;
        case PetType.noelle:
            return Noelle.possibleColors;
        case PetType.susie:
            return Susie.possibleColors;
        case PetType.spamton:
            return Spamton.possibleColors;
        case PetType.jevil:
            return Jevil.possibleColors;
        case PetType.tenna:
            return Tenna.possibleColors;
        default:
            throw new InvalidPetException("Pet type doesn't exist");
    }
}

/**
 * Some pets can only have certain colors, this makes sure they haven't been misconfigured.
 * @param petColor
 * @param petType
 * @returns normalized color
 */
export function normalizeColor(petColor: PetColor, petType: PetType): PetColor {
    const colors = availableColors(petType);
    if (colors.includes(petColor)) {
        return petColor;
    } else {
        return colors[0];
    }
}
