import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // ADR 001: Versionamento de rotas com prefixo global /v1
  app.setGlobalPrefix('v1');

  // ADR 001: Habilitar CORS com origem do front
  app.enableCors({
    origin: process.env.FRONTEND_URL || 'http://localhost:5173',
    credentials: true,
  });

  const port = process.env.PORT || 3000;
  await app.listen(port);
  console.log(`EMPREST.AI API está rodando na porta ${port}: http://localhost:${port}/v1/health`);
}

bootstrap();

