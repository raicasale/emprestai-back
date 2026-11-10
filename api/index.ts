import { NestFactory } from '@nestjs/core';
import { ExpressAdapter } from '@nestjs/platform-express';
import { AppModule } from '../src/app.module';
import express, { Request, Response } from 'express';

let cachedServer: (req: Request, res: Response) => void;

async function bootstrapServer(): Promise<(req: Request, res: Response) => void> {
  if (!cachedServer) {
    const expressApp = express();
    const adapter = new ExpressAdapter(expressApp);
    const app = await NestFactory.create(AppModule, adapter);

    app.setGlobalPrefix('v1', {
      exclude: ['/', 'health'],
    });

    app.enableCors({
      origin: process.env.FRONTEND_URL || '*',
      credentials: true,
    });

    await app.init();
    cachedServer = expressApp;
  }
  return cachedServer;
}

export default async function handler(req: Request, res: Response) {
  try {
    const server = await bootstrapServer();
    return server(req, res);
  } catch (err) {
    console.error('Erro na inicialização do NestJS:', err);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}
