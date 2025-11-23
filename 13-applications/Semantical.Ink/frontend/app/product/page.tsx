import { ProductHero } from '@/components/produce/ProductHero';
import { BlueprintSection } from '@/components/produce/BlueprintSection';
import { ProtectionSection } from '@/components/produce/ProtectionSection';
import { DerivativeSection } from '@/components/produce/DerivativeSection';
import { DashboardSection } from '@/components/produce/DashboardSection';
import { Footer } from '@/components/landing/Footer';

export default function ProducePage() {
  return (
    <main className="min-h-screen bg-brand-dark">
      <ProductHero />
      <BlueprintSection />
      <ProtectionSection />
      <DerivativeSection />
      <DashboardSection />
      <Footer />
    </main>
  );
}

