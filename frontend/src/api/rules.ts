import {request} from './client';import type {Rule} from '../types/entities';export const list=()=>request<Rule[]>('/rules');export const create=(data:unknown)=>request<Rule>('/rules','POST',data);
