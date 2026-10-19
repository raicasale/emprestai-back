import { PrismaClient, Role } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('Iniciando seed...');

  // 1. Criar tenant padrão 'suporte_ti' se não existir
  const tenant = await prisma.tenant.upsert({
    where: { slug: 'suporte_ti' },
    update: {},
    create: {
      slug: 'suporte_ti',
      name: 'Suporte de TI & Operações',
    },
  });

  console.log(`Tenant criado/encontrado: ${tenant.name} (${tenant.id})`);
  console.log('Seed finalizado com sucesso.');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });

