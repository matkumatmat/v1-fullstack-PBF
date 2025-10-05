// src/app/admin/manage/customer/onboard/page.tsx

import PageContainer from "@/components/layout/page-container";
import { CustomerOnboardWizard } from "./customer-onboard-wizard";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export default function OnboardCustomerPage() {
  return (
    <PageContainer>
      <div className="w-full max-w-4xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle>Onboarding Customer Baru</CardTitle>
            <CardDescription>
              Ikuti langkah-langkah berikut untuk mendaftarkan customer baru beserta detail dan struktur organisasinya.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <CustomerOnboardWizard />
          </CardContent>
        </Card>
      </div>
    </PageContainer>
  );
}