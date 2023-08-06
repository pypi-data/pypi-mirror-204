Development Plan
$$$$$$$$$$$$$$$$

This document presents the goals of the StrictDoc project and describes how the
project is developed.

Project goals
=============

StrictDoc is an attempt to create an open source tool for writing
technical requirements specifications.

.. _GOAL-1-TOOL-SUPPORT:

Software support for writing requirements and specifications documents
----------------------------------------------------------------------

.. list-table::
    :align: left
    :header-rows: 0

    * - **UID:**
      - GOAL-1-TOOL-SUPPORT

There shall exist free and lightweight yet capable software for writing
requirements and specifications documents

**Comment:** Technical documentation is hard, it can be an extremely laborious process.
Software shall support engineers in their work with documentation.

**Children:**

- ``[SDOC-HIGH-REQS-MANAGEMENT]`` :ref:`SDOC-HIGH-REQS-MANAGEMENT`

.. _GOAL-2-REDUCE-DOCUMENTATION-HAZARDS:

Reduce documentation hazards
----------------------------

.. list-table::
    :align: left
    :header-rows: 0

    * - **UID:**
      - GOAL-2-REDUCE-DOCUMENTATION-HAZARDS

There shall exist no (or less) opportunity for writing incorrect or inconsistent
documentation.

**Comment:** Every serious engineering activity, such as safety engineering or systems
engineering, starts with requirements. The more critical is a product the higher
the importance of good documentation.

Technical documentation can be and often becomes a source of hazards.
It is recognized that many failures stem from inadequate requirements
engineering. While it is not possible to fix the problem of inadequate
requirements engineering in general, it is definitely possible to improve
software that supports engineers in activities such as requirements engineering
and writing technical documentation.

.. _GOAL-3-NO-RUNAWAY-DOCUMENTATION:

No (or less) run-away documentation
-----------------------------------

.. list-table::
    :align: left
    :header-rows: 0

    * - **UID:**
      - GOAL-3-NO-RUNAWAY-DOCUMENTATION

Software shall support engineers in keeping documentation up-to-date.

**Comment:** Technical documentation easily becomes outdated. Many existing tools for
documentation do not provide any measures for ensuring overall consistency of
documents and documentation trees.

.. _GOAL-4-CHANGE-MANAGEMENT:

Change management
-----------------

.. list-table::
    :align: left
    :header-rows: 0

    * - **UID:**
      - GOAL-4-CHANGE-MANAGEMENT

Software shall provide capabilities for change management and impact assessment.

**Comment:** Change management is difficult. The bigger the project is, the harder it is to
maintain its documentation. If a change is introduced to a project, it usually
requires a full revision of its requirements.

**Comment:** When the basic capabilities of StrictDoc are in place, it should be possible
to do a more advanced analysis of requirements and requirement trees:

- Finding similar or relevant requirements.
- Enforce invariants that should be hold. Example: mass or power budget.

Project milestones
==================

As an open-source project, StrictDoc is developed without strict deadlines, however there are certain high-level priorities that influence the development. The work is loosely organized in quarters.

See also the Backlog document for a complete list of the planned work items.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - **Quarter**
     - **Planned / accomplished work**

   * - 2019-Q2
     - Pre-StrictDoc development in a fork of Doorstop.
   * - 2019-Q3
     - StrictDoc, first prototype. Markdown-based C++ program. Custom requirements metadata in YAML.
   * - 2020-Q1
     - The second prototype of StrictDoc based on RST/Sphinx. Using Sphinx extensions to manage meta information. First integration tests.
   * - 2020-Q2
     - StrictDoc created on GitHub. The code still uses RST for parsing requirements meta information and PySide for GUI.
   * - 2020-Q3
     - The RST parsing is replaced with a TextX-based DSL, new StrictDoc grammar is created. The PySide is replaced with a simple export to HTML using Jinja templates. Export to Sphinx HTML/PDF is introduced.
   * - 2020-Q4
     - Improvements in the styles of HTML/PDF exports. First Table, Traceability, and Deep Traceability screens.
   * - 2021-Q1
     - Excel export. The first implementation for forward and reverse traceability between SDoc and source files.
   * - 2021-Q2
     - Further work on the SDoc-source traceability.
   * - 2021-Q3
     - Further work on the SDoc-source traceability. Tree cycles detection, validations. MathJax support.
   * - 2021-Q4
     - Improvements of the traceability index generation and validation. Initial implementation of ReqIF. First support of custom grammars.
   * - 2022-Q1
     - Further work on ReqIF and custom grammars. Document fragments feature.
   * - 2022-Q2
     - Excel conversion improvements. Improvements of how meta information is displayed in HTML export.
   * - 2022-Q3
     - No work in this quarter.
   * - 2022-Q4
     - Installation using PyInstaller. The first prototype of a Web-based interface. First end-to-end Web tests using SeleniumBase. Improvements of the ReqIF support.
   * - 2023-Q1
     - Improvements of the Web-based interface towards first release. Improvements of the ReqIF support.
   * - 2023-Q2
     - Further stabilization of the Web interface. Improvements of the ReqIF interface.
