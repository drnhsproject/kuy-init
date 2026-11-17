export interface ButtonProps { label: string }
export type Size = 'sm' | 'lg';
export const DEFAULT_SIZE = 'sm';
// Render a button
export const Button = (props: ButtonProps) => <button>{props.label}</button>;
export function helper(a: number): number { return a; }
export class Store {
  private items: string[] = [];
  add(item: string): void { this.items.push(item); }
  if (x) {
}
