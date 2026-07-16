import React from 'react';
import { render } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import App from '../app/App';

vi.mock('../services/api', () => ({
  default: {
    get: vi.fn(() => new Promise(() => undefined)),
    post: vi.fn(),
  },
}));

describe('Hogar Express Application Bootstrapping', () => {
  it('renders loading screen initially', () => {
    const { getByText } = render(<App />);
    expect(getByText(/Cargando Hogar Express.../i)).toBeInTheDocument();
  });
});
