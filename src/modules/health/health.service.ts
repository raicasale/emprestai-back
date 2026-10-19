import { Injectable } from '@nestjs/common';

export interface HealthCheckResponse {
  status: string;
  timestamp: string;
  uptime: number;
}

@Injectable()
export class HealthService {
  private readonly startTime = Date.now();

  check(): HealthCheckResponse {
    const uptimeSeconds = (Date.now() - this.startTime) / 1000;
    return {
      status: 'ok',
      timestamp: new Date().toISOString(),
      uptime: Math.round(uptimeSeconds * 100) / 100,
    };
  }
}

