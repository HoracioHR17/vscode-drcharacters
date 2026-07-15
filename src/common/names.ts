import {
    JEVIL_NAMES,
    KRIS_NAMES,
    LANCER_NAMES,
    NOELLE_NAMES,
    RALSEI_NAMES,
    SPAMTON_NAMES,
    SUSIE_NAMES,
    TENNA_NAMES,
} from '../panel/pets/deltarune';
import { PetType } from './types';

export function randomName(type: PetType): string {
    const collection: ReadonlyArray<string> =
        (
            {
                [PetType.kris]: KRIS_NAMES,
                [PetType.lancer]: LANCER_NAMES,
                [PetType.ralsei]: RALSEI_NAMES,
                [PetType.noelle]: NOELLE_NAMES,
                [PetType.susie]: SUSIE_NAMES,
                [PetType.spamton]: SPAMTON_NAMES,
                [PetType.jevil]: JEVIL_NAMES,
                [PetType.tenna]: TENNA_NAMES,
            } as Record<PetType, ReadonlyArray<string>>
        )[type] ?? KRIS_NAMES;

    return (
        collection[Math.floor(Math.random() * collection.length)] ?? 'Unknown'
    );
}
