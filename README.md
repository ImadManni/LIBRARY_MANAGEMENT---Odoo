# Library Management System - Odoo Module

Le Système de Gestion de Bibliothèque constitue une réponse innovante et intégrée pour moderniser l'ensemble des opérations liées à la bibliothèque. Développé au moyen du framework Odoo, cette solution complète vise à optimiser la gestion des livres, des auteurs, des catégories, des copies, des emprunts, et des éditeurs d'une manière efficace et intuitive.

**The Library Management System is an innovative and integrated solution to modernize all library-related operations. Developed using the Odoo framework, this complete solution aims to optimize the management of books, authors, categories, copies, borrows, and publishers in an efficient and intuitive manner.**

## Architecture

Le système suit une architecture modulaire, avec des modules distincts pour la gestion des auteurs, des catégories, des copies de livres, des données de livres, des emprunts et des éditeurs. Chaque module est conçu pour répondre à des besoins spécifiques tout en permettant une intégration harmonieuse.

The system follows a modular architecture, with distinct modules for managing authors, categories, book copies, book data, borrows, and publishers. Each module is designed to meet specific needs while allowing seamless integration.

![Class Diagram](library_management_uml.puml)

> **Note:** To view the UML class diagram, use a PlantUML viewer or render the `library_management_uml.puml` file.

## Module Structure

```
library_management/
├── __init__.py                 # Module initialization
├── __manifest__.py             # Module manifest/configuration
├── README.md                   # This file
├── library_management_uml.puml # UML Class Diagram (PlantUML)
├── models/                     # Python ORM models
│   ├── __init__.py
│   ├── book.py                # Book model (Books_data)
│   ├── reader.py              # Reader model
│   └── loan.py                # Loan model (Borrows)
├── views/                      # XML views
│   ├── book_views.xml         # Book views (tree, form, kanban)
│   ├── reader_views.xml       # Reader views (tree, form, kanban)
│   ├── loan_views.xml         # Loan views (tree, form, kanban)
│   └── menu_views.xml         # Menu structure
└── security/                   # Security rules
    └── ir.model.access.csv    # Access rights
```

## Database Schema

The system includes the following main entities:

- **Author** (`library.author`): Manages author information, tracks employment dates, and computes age
- **Books_data** (`library.book.data`): Main book information entity with links to Author and Category
- **Book_Category** (`library.book.category`): Categorizes books for better organization
- **BookCopies** (`library.book.copy`): Individual physical copies of books with state tracking
- **Borrows** (`library.borrow`): Loan/borrowing transactions with fee calculation

See `library_management_uml.puml` for the complete class diagram with relationships and cardinalities.

## Installation

1. Copy the `library_management` folder to your Odoo addons directory
2. Update the apps list in Odoo
3. Search for "Library Management" in Apps
4. Click Install

## Fonctionnalités clés / Key Features

1. **Recherche de Livres / Book Search**: Les utilisateurs peuvent rechercher des livres en fonction du titre, de l'auteur, State, etc. Possibilité de filtrer les résultats pour affiner la recherche.
   Users can search for books by title, author, state, etc. Results can be filtered to refine the search.

2. **Consultation des Détails des Livres / Book Details**: Accès aux détails complets des livres, y compris la description, la langue, la version, le nombre de pages, etc.
   Access to complete book details, including description, language, version, number of pages, etc.

3. **Gestion des Catégories / Category Management**: Exploration des livres par catégorie.
   Explore books by category.

4. **Découverte des Auteurs / Author Discovery**: Consultation des informations sur les auteurs. Accès aux livres associés à chaque auteur.
   View author information. Access books associated with each author.

5. **Emprunts de Livres / Book Borrowing**: 
   - Possibilité d'emprunter des livres en fonction de la disponibilité des copies
   - Suivi des dates de début et de fin de l'emprunt
   - Visualisation des emprunts en cours, des emprunts passés et des emprunts en attente
   
   - Ability to borrow books based on copy availability
   - Track start and end dates of borrows
   - View current, past, and pending borrows

6. **Gestion des Copies / Copy Management**: 
   - Vérification de l'état des copies (disponible, emprunté, perdu, etc.)
   - Affichage rapide des copies disponibles
   
   - Check copy state (available, borrowed, lost, etc.)
   - Quick display of available copies

7. **Rapports d'Activité / Activity Reports**: Consultation de rapports détaillés sur les emprunts. Visualisation graphique de l'activité de la bibliothèque.
   View detailed reports on borrows. Graphical visualization of library activity.

8. **Tableau de Bord Personnalisé / Custom Dashboard**: Vue d'ensemble du tableau de bord avec des informations cruciales, y compris les emprunts en cours, les livres les plus empruntés, etc.
   Dashboard overview with crucial information, including current borrows, most borrowed books, etc.

9. **Interaction Intuitive / Intuitive Interface**: Interface utilisateur conviviale avec des boutons d'action clairs pour les opérations courantes (emprunter, retourner, etc.).
   User-friendly interface with clear action buttons for common operations (borrow, return, etc.).

10. **Calendrier des Emprunts / Borrow Calendar**: Visualisation des emprunts sur un calendrier pour une gestion temporelle facile.
    View borrows on a calendar for easy temporal management.

11. **Facilité de Navigation / Easy Navigation**: Navigation aisée à travers les menus pour accéder rapidement aux différentes fonctionnalités.
    Easy navigation through menus to quickly access different features.

## Usage

1. **Add Books**: Go to Library > Books and create book records
2. **Register Readers**: Go to Library > Readers and add library members
3. **Create Loans**: Go to Library > Loans to borrow books to readers
4. **Return Books**: Use the "Return Book" button in loan forms

## Technical Details

- **Odoo Version**: 16.0+
- **Python Version**: 3.8+
- **Dependencies**: base module only
- **License**: LGPL-3

## UML Class Diagram

This project includes a comprehensive UML class diagram in PlantUML format (`library_management_uml.puml`). The diagram shows:

- All entity classes with their attributes and methods
- Relationships between entities with cardinalities
- Odoo model names and descriptions
- Primary keys (PK) and foreign keys (FK) annotations

To view the diagram:
- Use an online PlantUML viewer: http://www.plantuml.com/plantuml/uml/
- Install PlantUML extension in VS Code
- Use PlantUML command line tool: `java -jar plantuml.jar library_management_uml.puml`

## Contributing

This is an academic project for library management system development using Odoo framework.

## References

Inspired by similar Odoo library management implementations and best practices in ERP system development.

