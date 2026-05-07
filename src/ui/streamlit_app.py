from __future__ import annotations

import streamlit as st

from src.app.orchestrator import Orchestrator
from src.config.settings import settings


def main() -> None:
    st.title("Autonomous Multi-Agent AI Research Assistant")
    topic = st.text_input("Topic", value="Explain BERT vs GPT")
    max_sources = st.slider("Max sources", 2, 20, 8)
    max_chunks = st.slider("Max chunks", 5, 100, 30)
    export_pdf = st.checkbox("Export PDF", value=False)
    dry_run = st.checkbox("Dry run", value=False)

    if st.button("Run pipeline"):
        with st.spinner("Running planner -> research -> writer -> reviewer -> report..."):
            orchestrator = Orchestrator(settings=settings)
            result = orchestrator.run(
                topic=topic,
                max_sources=max_sources,
                max_chunks=max_chunks,
                export_pdf=export_pdf,
                dry_run=dry_run,
            )
        st.success(f"Completed run {result.run_id}")
        st.code(result.final_markdown_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
