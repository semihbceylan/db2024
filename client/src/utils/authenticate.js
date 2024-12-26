import { client } from '@passwordless-id/webauthn';
import { random, floor } from 'mathjs';

function randomChallangeGenerator () {
    let buffer = new Uint8Array(18); for (let i = 0; i < 18; i++) {buffer[i] = floor(random(0, 255));}
    const txt = btoa(String.fromCharCode(...new Uint8Array(buffer)));
    return txt.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export default async function authenticate () {
    try {return (await client.authenticate({challenge: randomChallangeGenerator()})).id == import.meta.env.VITE_ADMIN_ID;}
    catch {return false;}
}