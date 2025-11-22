import { Hero } from '@/components/landing/Hero';
import { WhatIsSection } from '@/components/landing/WhatIsSection';
import { HowItWorksSection } from '@/components/landing/HowItWorksSection';
import { UseCasesSection } from '@/components/landing/UseCasesSection';
import { MarketplaceSection } from '@/components/landing/MarketplaceSection';
import { WhyMattersSection } from '@/components/landing/WhyMattersSection';
import { Footer } from '@/components/landing/Footer';

export default function Home() {
  return (
    <main className="min-h-screen bg-white">
      <Hero />
      <WhatIsSection />
      <HowItWorksSection />
      <UseCasesSection />
      <MarketplaceSection />
      <WhyMattersSection />
      <Footer />
    </main>
  );
}
