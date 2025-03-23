DROP DATABASE IF EXISTS BoardGame;

CREATE DATABASE BoardGame;

USE BoardGame;


CREATE TABLE universities (
    UniversityID INT AUTO_INCREMENT PRIMARY KEY,
    UniversityName VARCHAR(255) NOT NULL,
    Location VARCHAR(255) NOT NULL,
    LogoURL VARCHAR(512),
    BannerURL VARCHAR(512),
    Description TEXT NOT NULL,
    WebsiteURL VARCHAR(255) NOT NULL
);


CREATE TABLE roles (
    RoleID INT AUTO_INCREMENT PRIMARY KEY,
    RoleName VARCHAR(50) NOT NULL UNIQUE,
    Description TEXT NOT NULL
);


CREATE TABLE users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Username VARCHAR(255) NOT NULL UNIQUE,
    Email VARCHAR(255) NOT NULL UNIQUE,
    FirebaseUID VARCHAR(128) NOT NULL UNIQUE,
    ProfileImageURL VARCHAR(255),
    Bio TEXT,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Paid BOOLEAN NOT NULL DEFAULT FALSE,
    TeamID INT NULL,
    RoleID INT NOT NULL,
    UniversityID INT NULL,
    IsValidated BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (RoleID) REFERENCES roles(RoleID),
    FOREIGN KEY (UniversityID) REFERENCES universities(UniversityID)
);

-- Create Teams table without the foreign key constraint for TeamLeaderID
CREATE TABLE teams (
    TeamID INT AUTO_INCREMENT PRIMARY KEY,
    UniversityID INT NOT NULL,
    TeamName VARCHAR(255) NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ProfileImageURL VARCHAR(255),
    Description TEXT,
    TeamLeaderID INT NOT NULL,
    IsApproved BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (UniversityID) REFERENCES universities(UniversityID)
);


CREATE TABLE tournaments (
    TournamentID INT AUTO_INCREMENT PRIMARY KEY,
    TournamentName VARCHAR(255) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    Status ENUM('Active', 'Completed', 'Cancelled', 'Upcoming') NOT NULL,
    Location VARCHAR(255) NOT NULL
);


CREATE TABLE matches (
    MatchID INT AUTO_INCREMENT PRIMARY KEY,
    TournamentID INT NOT NULL,
    Team1ID INT NOT NULL,
    Team2ID INT NOT NULL,
    Score1 INT NOT NULL DEFAULT 0,
    Score2 INT NOT NULL DEFAULT 0,
    WinnerID INT,
    MatchTime DATETIME NOT NULL,
    FOREIGN KEY (TournamentID) REFERENCES tournaments(TournamentID),
    FOREIGN KEY (Team1ID) REFERENCES teams(TeamID),
    FOREIGN KEY (Team2ID) REFERENCES teams(TeamID),
    FOREIGN KEY (WinnerID) REFERENCES teams(TeamID)
);


CREATE TABLE tournament_participants (
    TournamentID INT NOT NULL,
    TeamID INT NOT NULL,
    Round INT NOT NULL DEFAULT 0,
    Byes INT NOT NULL DEFAULT 0,
    Status ENUM('active', 'lost', 'winner', 'disqualified') NOT NULL DEFAULT 'active',
    BracketSide ENUM('left', 'right') NOT NULL DEFAULT 'left', 
    NextMatchID INT NULL,
    BracketOrder INT NOT NULL DEFAULT 0,
    PRIMARY KEY (TournamentID, TeamID),
    FOREIGN KEY (TournamentID) REFERENCES tournaments(TournamentID),
    FOREIGN KEY (TeamID) REFERENCES teams(TeamID)
);



CREATE TABLE tournament_facilitators (
    TournamentID INT NOT NULL,
    UserID INT NOT NULL,
    PRIMARY KEY (TournamentID, UserID),
    FOREIGN KEY (TournamentID) REFERENCES tournaments(TournamentID),
    FOREIGN KEY (UserID) REFERENCES users(UserID)
);


CREATE TABLE tickets (
    TicketID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Subject VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    Status ENUM('Open', 'In Progress', 'Closed') NOT NULL DEFAULT 'Open',
    TicketType ENUM('Bug Report', 'User Report', 'General Inquiry', 'Approval Request') NOT NULL,
    ReportedUserID INT,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES users(UserID),
    FOREIGN KEY (ReportedUserID) REFERENCES users(UserID)
);

CREATE TABLE user_update (
    UserUpdateId INT AUTO_INCREMENT PRIMARY KEY,
    UpdatedUserID INT NOT NULL,
    ApprovedBy INT NULL,
    RequestedDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FirstName VARCHAR(255) NULL,
    LastName VARCHAR(255) NULL,
    Username VARCHAR(255) NULL,
    Email VARCHAR(255) NULL,
    ProfileImageURL VARCHAR(255) NULL,
    Bio TEXT NULL,
    FOREIGN KEY (UpdatedUserID) REFERENCES users(UserID),
    FOREIGN KEY (ApprovedBy) REFERENCES users(UserID)
);

CREATE TABLE team_update (
    TeamUpdateId INT AUTO_INCREMENT PRIMARY KEY,
    UpdatedTeamID INT NOT NULL,
    ApprovedBy INT NULL,
    RequestedDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    TeamName VARCHAR(255) NULL,
    ProfileImageURL VARCHAR(255) NULL,
    Description TEXT NULL,
    FOREIGN KEY (UpdatedTeamID) REFERENCES teams(TeamID),
    FOREIGN KEY (ApprovedBy) REFERENCES users(UserID)
);

-- Add foreign key for TeamLeaderID in tblTeams
ALTER TABLE teams
ADD CONSTRAINT FK_Teams_TeamLeaderID FOREIGN KEY (TeamLeaderID) REFERENCES users(UserID);

-- Add foreign key for TeamID in tblUsers
ALTER TABLE users
ADD CONSTRAINT FK_Users_TeamID FOREIGN KEY (TeamID) REFERENCES teams(TeamID);


-- Indexes for foreign key columns
CREATE INDEX idx_users_university_id ON users (UniversityID);
CREATE INDEX idx_users_role_id ON users (RoleID);
CREATE INDEX idx_teams_university_id ON teams (UniversityID);
CREATE INDEX idx_teams_team_leader_id ON teams (TeamLeaderID);
CREATE INDEX idx_matches_tournament_id ON matches (TournamentID);
CREATE INDEX idx_matches_team1_id ON matches (Team1ID);
CREATE INDEX idx_matches_team2_id ON matches (Team2ID);
CREATE INDEX idx_tournament_participants_tournament_id ON tournament_participants (TournamentID);
CREATE INDEX idx_tournament_participants_team_id ON tournament_participants (TeamID);
CREATE INDEX idx_tournament_facilitators_tournament_id ON tournament_facilitators (TournamentID);
CREATE INDEX idx_tournament_facilitators_user_id ON tournament_facilitators (UserID);
CREATE INDEX idx_tickets_user_id ON tickets (UserID);
CREATE INDEX idx_tickets_reported_user_id ON tickets (ReportedUserID);

-- Indexes for frequently queried columns
CREATE INDEX idx_tournaments_tournament_name ON tournaments (TournamentName);
CREATE INDEX idx_users_username ON users (Username);
CREATE INDEX idx_users_email ON users (Email);
