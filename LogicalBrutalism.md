# Brutalismo Lógico (v1.1)

> [cite_start]"O que não resolve, não existe." [cite: 3, 25, 462]

[cite_start]Um sistema de design para contextos de alta densidade de informação (IDEs, dashboards, ferramentas internas)[cite: 4, 31]. [cite_start]Baseado na premissa de que a **verdade técnica é uma forma legítima de estética em software**[cite: 21].

[cite_start]Aqui, remove-se até só restar a função[cite: 29]. [cite_start]Cada decisão visual custa uma justificativa funcional[cite: 24].

## 🏛️ Fundação Filosófica (Axiomas)

[cite_start]Todas as decisões do sistema derivam de como humanos processam informação, não de preferência estética[cite: 37]:

1. **Função Precede Forma:** Se um elemento não transmite informação ou guia uma ação, ele é ruído cognitivo. [cite_start]Beleza é consequência, nunca objetivo[cite: 40, 42].
2. **Estrutura Exposta:** A lógica do sistema (hierarquia, estado, comportamento) deve ser legível em menos de 100ms. [cite_start]O sistema não esconde como funciona[cite: 46, 48].
3. [cite_start]**Restrição Como Ferramenta:** Menos opções = mais consistência e menor carga cognitiva[cite: 52].

## 🎨 Sistema de Cores (Hierarquia de Atenção)

A paleta usa apenas 6 tokens. [cite_start]A cor é consequência do estado, nunca uma escolha independente[cite: 52, 59, 137].

- `--color-void` (`#0A0A0A`): Fundo principal. [cite_start]Ausência de ruído[cite: 67, 87].
- `--color-amber` (`#FFB000`): **Único acento de ação.** Reservado para CTAs primários e estados ativos (Ref: Fósforo P3, anos 1970). [cite_start]Regra: Apenas UM elemento âmbar por tela[cite: 69, 70, 71, 154].
- `--color-surface` (`#1E1E1E`): Separação de contexto e bordas. [cite_start]Nunca iterativo[cite: 73, 88].
- [cite_start]`--color-text` (`#888888`): Leitura contínua[cite: 75, 89].
- [cite_start]`--color-white` (`#F0F0F0`): Ênfase máxima (títulos, dados críticos)[cite: 78, 90].
- [cite_start]`--color-error` (`#FF4444`): Uso exclusivo para erros e alertas críticos[cite: 80, 91].

## 🔤 Tipografia: Duas Camadas

[cite_start]A escolha da fonte distingue o "quem fala" (o sistema ou o humano)[cite: 148, 150].

- **Camada Lógica (Sistema):** `JetBrains Mono`. [cite_start]Usada para dados brutos, código, labels, status e timestamps[cite: 100, 102, 149].
- **Camada Humana (Conteúdo):** `Inter`. [cite_start]Usada para blocos de texto e leitura contínua[cite: 97, 99, 150].

## ⚙️ Princípios Gerativos

[cite_start]Critérios práticos de execução durante o desenvolvimento[cite: 133]:

- **Ângulo como compromisso:** Bordas de 90 graus (`border-radius: 0`). [cite_start]O sistema não suaviza a realidade[cite: 143, 146].
- [cite_start]**Espaço é silêncio:** O espaçamento comunica relação lógica (contexto), não apenas "preenchimento visual"[cite: 163, 164].
- **Feedback imediato e honesto:** Não há transições suaves (`transition: none`). [cite_start]Os estados são discretos[cite: 169, 197, 215].
- [cite_start]**ASCII antes de Ícone:** Use texto puro (`[+]`, `[x]`, `[>]`) no lugar de SVGs externos para zero overhead, recorrendo a ícones apenas quando estritamente necessário[cite: 175, 176, 302].

## ♿ Acessibilidade Integrada

[cite_start]Não é concessão, é consistência com o Axioma I. Uma interface ilegível falhou na função[cite: 307, 308].

- [cite_start]Contrastes validados WCAG AA e AAA out-of-the-box[cite: 309, 402].
- [cite_start]Touch targets com mínimo de 44px[cite: 318, 357].
- [cite_start]Estados de erro dependem de 4 camadas (código, título, descrição, ação), nunca apenas da cor[cite: 223, 225, 243].

---

[cite_start]**Status:** Documento Vivo (v1.1.0) [cite: 11, 12, 459, 461]
[cite_start]**Criado por:** Matheus Lacerda [cite: 6, 454]
