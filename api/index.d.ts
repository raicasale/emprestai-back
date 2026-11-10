import express, { Request, Response } from 'express';
export default function handler(req: Request, res: Response): Promise<void | express.Response<any, Record<string, any>>>;
