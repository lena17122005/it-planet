import { useEffect, useState } from 'react';
import type { Vacancy } from '../types';

const mockVacancies: Vacancy[] = [
  {
    id: '1',
    title: 'Frontend Intern',
    company: 'Tech Start',
    city: 'Москва',
    salaryFrom: 60000,
    salaryTo: 90000,
    lat: 55.751244,
    lng: 37.618423,
    format: 'hybrid',
    type: 'internship',
    tags: ['React', 'TypeScript']
  }
];

export function useVacancies() {
  const [vacancies, setVacancies] = useState<Vacancy[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      setVacancies(mockVacancies);
      setIsLoading(false);
    }, 300);

    return () => clearTimeout(timeoutId);
  }, []);

  return { vacancies, isLoading };
}
