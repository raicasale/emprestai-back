import { Controller, Get } from '@nestjs/common';
import { HealthService, HealthCheckResponse } from './health.service';

@Controller()
export class HealthController {
  constructor(private readonly healthService: HealthService) {}

  @Get(['health', 'v1/health', '/'])
  check(): HealthCheckResponse {
    return this.healthService.check();
  }
}
