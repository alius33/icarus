import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import MarkdownContent from '@/components/MarkdownContent';

describe('MarkdownContent', () => {
  it('renders markdown text as HTML', () => {
    render(<MarkdownContent>**bold text**</MarkdownContent>);
    const bold = screen.getByText('bold text');
    expect(bold).toBeInTheDocument();
    expect(bold.tagName).toBe('STRONG');
  });

  it('renders a heading from markdown', () => {
    render(<MarkdownContent>{'# Hello World'}</MarkdownContent>);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('Hello World');
  });

  it('renders a list from markdown', () => {
    const md = '- item one\n- item two\n- item three';
    render(<MarkdownContent>{md}</MarkdownContent>);
    const items = screen.getAllByRole('listitem');
    expect(items).toHaveLength(3);
    expect(items[0]).toHaveTextContent('item one');
    expect(items[1]).toHaveTextContent('item two');
    expect(items[2]).toHaveTextContent('item three');
  });

  it('renders a GFM table (via remark-gfm)', () => {
    const md = '| Col A | Col B |\n|-------|-------|\n| 1 | 2 |';
    render(<MarkdownContent>{md}</MarkdownContent>);
    const table = screen.getByRole('table');
    expect(table).toBeInTheDocument();
    expect(screen.getByText('Col A')).toBeInTheDocument();
    expect(screen.getByText('Col B')).toBeInTheDocument();
  });

  it('renders empty content gracefully', () => {
    const { container } = render(<MarkdownContent>{''}</MarkdownContent>);
    // The wrapper div should still exist with the prose classes
    const wrapper = container.firstElementChild;
    expect(wrapper).toBeInTheDocument();
    expect(wrapper?.className).toContain('prose');
  });

  it('applies custom className alongside default prose classes', () => {
    const { container } = render(
      <MarkdownContent className="my-custom-class">
        Some content
      </MarkdownContent>,
    );
    const wrapper = container.firstElementChild;
    expect(wrapper?.className).toContain('prose');
    expect(wrapper?.className).toContain('my-custom-class');
  });

  it('renders a link from markdown', () => {
    render(
      <MarkdownContent>{'[click here](https://example.com)'}</MarkdownContent>,
    );
    const link = screen.getByRole('link', { name: 'click here' });
    expect(link).toBeInTheDocument();
    expect(link).toHaveAttribute('href', 'https://example.com');
  });

  it('renders inline code from markdown', () => {
    render(<MarkdownContent>{'Use `console.log()` for debugging'}</MarkdownContent>);
    const code = screen.getByText('console.log()');
    expect(code).toBeInTheDocument();
    expect(code.tagName).toBe('CODE');
  });
});
