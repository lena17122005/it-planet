export type Role = 'seeker' | 'employer' | 'curator';

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
  salaryFrom?: number;
  salaryTo?: number;
  lat: number;
  lng: number;
  format: 'office' | 'hybrid' | 'remote';
  type: 'vacancy' | 'internship' | 'event' | 'mentorship';
  tags: string[];
}
