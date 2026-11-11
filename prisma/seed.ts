import 'dotenv/config';
import { PrismaClient, EquipmentStatus, Role } from '@prisma/client';

const prisma = new PrismaClient();

// ============================================================================
// DADOS INICIAIS DA PRÁTICA (ENTREGA 3)
// ============================================================================

// Credenciais obrigatórias do professor (conforme item 5 do briefing da Entrega 3:
// "Para facilitar a correção, deixe a senha escrita no próprio arquivo que popula os dados.")
export const PROFESSOR_CREDENTIALS = {
  email: 'marcelo.grilo@institutojef.org.br',
  password: 'Inovacao2026',
  role: Role.COLLABORATOR,
};

// 12 Equipamentos definidos pelo enunciado da prática
// Nota de decisão (Seção 1 / 1b do ENTREGA.md):
// O briefing texto dizia "TI-0004 e TI-0007 em manutenção; os outros 10 disponíveis",
// enquanto o JSON detalhado continha TI-0010 como manutenção.
// Decisão: mantemos TI-0004, TI-0007 e TI-0010 como MAINTENANCE conforme o JSON oficial.
export const EQUIPAMENTOS_INICIAIS = [
  { patrimonio: 'TI-0001', nome: 'Notebook 14 polegadas', categoria: 'notebook', status: EquipmentStatus.AVAILABLE, busca: 'laptop on white desk' },
  { patrimonio: 'TI-0002', nome: 'Notebook 15 polegadas', categoria: 'notebook', status: EquipmentStatus.AVAILABLE, busca: 'open laptop minimal desk' },
  { patrimonio: 'TI-0003', nome: 'Notebook 13 polegadas', categoria: 'notebook', status: EquipmentStatus.AVAILABLE, busca: 'laptop closeup keyboard' },
  { patrimonio: 'TI-0004', nome: 'Notebook 15 polegadas', categoria: 'notebook', status: EquipmentStatus.MAINTENANCE, busca: 'closed laptop on table' },
  { patrimonio: 'TI-0005', nome: 'Monitor 24 polegadas', categoria: 'monitor', status: EquipmentStatus.AVAILABLE, busca: 'computer monitor on desk' },
  { patrimonio: 'TI-0006', nome: 'Monitor 27 polegadas', categoria: 'monitor', status: EquipmentStatus.AVAILABLE, busca: 'monitor screen office desk' },
  { patrimonio: 'TI-0007', nome: 'Monitor 22 polegadas', categoria: 'monitor', status: EquipmentStatus.MAINTENANCE, busca: 'black computer screen' },
  { patrimonio: 'TI-0008', nome: 'Cabo HDMI 2 m', categoria: 'cabo', status: EquipmentStatus.AVAILABLE, busca: 'hdmi cable' },
  { patrimonio: 'TI-0009', nome: 'Cabo USB-C 1 m', categoria: 'cabo', status: EquipmentStatus.AVAILABLE, busca: 'usb cable white background' },
  { patrimonio: 'TI-0010', nome: 'Cabo de rede 3 m', categoria: 'cabo', status: EquipmentStatus.MAINTENANCE, busca: 'ethernet cable' },
  { patrimonio: 'TI-0011', nome: 'Webcam Full HD', categoria: 'camera', status: EquipmentStatus.AVAILABLE, busca: 'webcam' },
  { patrimonio: 'TI-0012', nome: 'Câmera compacta', categoria: 'camera', status: EquipmentStatus.AVAILABLE, busca: 'compact camera on table' },
];

async function getOrCreateSupabaseUser(supabaseUrl?: string, serviceRoleKey?: string): Promise<string> {
  if (!supabaseUrl || !serviceRoleKey) {
    console.log('[Seed] Supabase URL ou Service Role Key ausentes. Usando ID determinístico local.');
    return 'usr-marcelo-grilo-local';
  }

  try {
    // 1. Tenta criar usuário no Supabase Auth via Admin API
    const createRes = await fetch(`${supabaseUrl}/auth/v1/admin/users`, {
      method: 'POST',
      headers: {
        'apikey': serviceRoleKey,
        'Authorization': `Bearer ${serviceRoleKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: PROFESSOR_CREDENTIALS.email,
        password: PROFESSOR_CREDENTIALS.password,
        email_confirm: true,
        user_metadata: { name: 'Prof. Marcelo Grilo' },
      }),
    });

    if (createRes.ok) {
      const user = await createRes.json() as { id: string };
      console.log(`[Seed] Usuário do professor criado no Supabase Auth: ${user.id}`);
      return user.id;
    }

    // 2. Se já existir (status 422), busca os usuários existentes
    const listRes = await fetch(`${supabaseUrl}/auth/v1/admin/users?page=1&per_page=50`, {
      headers: {
        'apikey': serviceRoleKey,
        'Authorization': `Bearer ${serviceRoleKey}`,
      },
    });

    if (listRes.ok) {
      const data = await listRes.json() as { users: Array<{ id: string; email: string }> };
      const found = data.users.find((u) => u.email === PROFESSOR_CREDENTIALS.email);
      if (found) {
        console.log(`[Seed] Usuário do professor já existe no Supabase Auth: ${found.id}`);
        return found.id;
      }
    }
  } catch (err) {
    console.warn('[Seed] Aviso: Não foi possível conectar à API do Supabase Auth:', err);
  }

  return 'usr-marcelo-grilo-local';
}

async function main() {
  console.log('====================================================');
  console.log('Iniciando Seed Idempotente — EMPREST.AI (Entrega 3)');
  console.log('====================================================');

  let rawUrl = (process.env.SUPABASE_URL || '').trim();
  if (rawUrl.startsWith('db.')) {
    rawUrl = rawUrl.replace(/^db\./, '');
  }
  if (rawUrl && !rawUrl.startsWith('http')) {
    rawUrl = `https://${rawUrl}`;
  }
  const supabaseUrl = rawUrl || 'https://stubxpftqcfiqqvsrplv.supabase.co';
  const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

  // 1. Tenant padrão 'suporte_ti'
  const tenant = await prisma.tenant.upsert({
    where: { slug: 'suporte_ti' },
    update: { name: 'Suporte de TI & Operações' },
    create: {
      slug: 'suporte_ti',
      name: 'Suporte de TI & Operações',
    },
  });
  console.log(`✓ Tenant configurado: ${tenant.name} (${tenant.id})`);

  // 2. Usuário obrigatório do Professor
  const professorUserId = await getOrCreateSupabaseUser(supabaseUrl, serviceRoleKey);
  const membership = await prisma.membership.upsert({
    where: {
      tenantId_userId: {
        tenantId: tenant.id,
        userId: professorUserId,
      },
    },
    update: {
      role: PROFESSOR_CREDENTIALS.role,
    },
    create: {
      tenantId: tenant.id,
      userId: professorUserId,
      role: PROFESSOR_CREDENTIALS.role,
    },
  });
  console.log(`✓ Membership do Professor garantido: ${membership.id} (Role: ${membership.role})`);

  // Confere que o professor começa com zero empréstimos
  const professorLoansCount = await prisma.loan.count({
    where: {
      membershipId: membership.id,
      status: 'ACTIVE',
    },
  });
  console.log(`✓ Empréstimos ativos do Professor: ${professorLoansCount} (esperado: 0)`);

  // 3. Os 12 Equipamentos (Idempotente com upsert por tenantId_code)
  console.log(`\nPopulando os 12 equipamentos no tenant ${tenant.slug}...`);
  for (const eq of EQUIPAMENTOS_INICIAIS) {
    const publicImageUrl = `${supabaseUrl}/storage/v1/object/public/equipamentos/${eq.patrimonio}.jpg`;
    const descriptionText = `Equipamento de ${eq.categoria}. Imagem pública: ${publicImageUrl}`;

    await prisma.equipment.upsert({
      where: {
        tenantId_code: {
          tenantId: tenant.id,
          code: eq.patrimonio,
        },
      },
      update: {
        name: eq.nome,
        category: eq.categoria,
        status: eq.status,
        description: descriptionText,
      },
      create: {
        tenantId: tenant.id,
        code: eq.patrimonio,
        name: eq.nome,
        category: eq.categoria,
        status: eq.status,
        description: descriptionText,
      },
    });

    const statusBadge = eq.status === EquipmentStatus.AVAILABLE ? '[DISPONÍVEL]' : '[MANUTENÇÃO]';
    console.log(`  ✓ ${eq.patrimonio}: ${eq.nome} ${statusBadge}`);
  }

  const totalCount = await prisma.equipment.count({ where: { tenantId: tenant.id } });
  const availableCount = await prisma.equipment.count({ where: { tenantId: tenant.id, status: EquipmentStatus.AVAILABLE } });
  const maintenanceCount = await prisma.equipment.count({ where: { tenantId: tenant.id, status: EquipmentStatus.MAINTENANCE } });

  console.log('====================================================');
  console.log('Seed finalizado com sucesso!');
  console.log(`Total de equipamentos cadastrados: ${totalCount}`);
  console.log(`  - Disponíveis: ${availableCount}`);
  console.log(`  - Em manutenção: ${maintenanceCount}`);
  console.log('====================================================');
}

main()
  .catch((e) => {
    console.error('[Seed Error]:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
