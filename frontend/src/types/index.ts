export type Role = 'seeker' | 'employer' | 'curator';

export type WorkFormat = 'office' | 'hybrid' | 'remote';
export type OpportunityType = 'vacancy' | 'internship' | 'event' | 'mentorship';

export interface AuthUser {
  id: string;
  email: string;
  displayName: string;
  role: Role;
}

export interface Vacancy {
  id: string;
  title: string;
  company: string;
  city: string;
  address?: string;
  description: string;
  requirements?: string;
  salaryFrom?: number;
  salaryTo?: number;
  lat: number;
  lng: number;
  format: WorkFormat;
  type: OpportunityType;
  tags: string[];
  expiresAt?: string;
  eventDate?: string;
}

export interface VacancyFilters {
  query: string;
  city: string;
  salaryFrom?: number;
  salaryTo?: number;
  format: 'all' | WorkFormat;
  tags: string;
}
