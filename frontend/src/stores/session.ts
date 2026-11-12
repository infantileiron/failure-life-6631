import type {User} from '../types/entities';
export function savedUser():User|null {try{return JSON.parse(sessionStorage.getItem('life-user')||'null')}catch{return null}}
export function saveSession(token:string,user:User){sessionStorage.setItem('life-token',token);sessionStorage.setItem('life-user',JSON.stringify(user))}
export function clearSession(){sessionStorage.removeItem('life-token');sessionStorage.removeItem('life-user')}
