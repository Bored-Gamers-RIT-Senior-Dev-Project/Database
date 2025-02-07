DROP DATABASE IF EXISTS BoardGame

CREATE DATABASE BoardGame

USE BoardGame


CREATE TABLE Universities (
    UniversityID INT AUTO_INCREMENT PRIMARY KEY,
    UniversityName VARCHAR(255) NOT NULL,
    Location VARCHAR(255) NOT NULL,
    LogoURL VARCHAR(255),
    BannerURL VARCHAR(255),
    Description TEXT NOT NULL,
    WebsiteURL VARCHAR(255) NOT NULL
);


CREATE TABLE Roles (
    RoleID INT AUTO_INCREMENT PRIMARY KEY,
    RoleName VARCHAR(50) NOT NULL UNIQUE,
    Description TEXT NOT NULL
);


CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
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
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID),
    FOREIGN KEY (UniversityID) REFERENCES Universities(UniversityID)
);

-- Create Teams table without the foreign key constraint for TeamLeaderID
CREATE TABLE Teams (
    TeamID INT AUTO_INCREMENT PRIMARY KEY,
    UniversityID INT NOT NULL,
    TeamName VARCHAR(255) NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ProfileImageURL VARCHAR(255),
    Description TEXT,
    TeamLeaderID INT NOT NULL,
    IsApproved BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (UniversityID) REFERENCES Universities(UniversityID)
);


CREATE TABLE Tournaments (
    TournamentID INT AUTO_INCREMENT PRIMARY KEY,
    TournamentName VARCHAR(255) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    Status ENUM('Active', 'Completed', 'Cancelled', 'Upcoming') NOT NULL,
    Location VARCHAR(255) NOT NULL
);


CREATE TABLE Matches (
    MatchID INT AUTO_INCREMENT PRIMARY KEY,
    TournamentID INT NOT NULL,
    Team1ID INT NOT NULL,
    Team2ID INT NOT NULL,
    Score1 INT NOT NULL DEFAULT 0,
    Score2 INT NOT NULL DEFAULT 0,
    WinnerID INT,
    MatchTime DATETIME NOT NULL,
    FOREIGN KEY (TournamentID) REFERENCES Tournaments(TournamentID),
    FOREIGN KEY (Team1ID) REFERENCES Teams(TeamID),
    FOREIGN KEY (Team2ID) REFERENCES Teams(TeamID),
    FOREIGN KEY (WinnerID) REFERENCES Teams(TeamID)
);


CREATE TABLE TournamentParticipants (
    TournamentID INT NOT NULL,
    UserID INT NOT NULL,
    PRIMARY KEY (TournamentID, UserID),
    FOREIGN KEY (TournamentID) REFERENCES Tournaments(TournamentID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);


CREATE TABLE Tickets (
    TicketID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Subject VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    Status ENUM('Open', 'In Progress', 'Closed') NOT NULL DEFAULT 'Open',
    TicketType ENUM('Bug Report', 'User Report', 'General Inquiry', 'Approval Request') NOT NULL,
    ReportedUserID INT,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ReportedUserID) REFERENCES Users(UserID)
);

-- Add foreign key for TeamLeaderID in tblTeams
ALTER TABLE Teams
ADD CONSTRAINT FK_Teams_TeamLeaderID FOREIGN KEY (TeamLeaderID) REFERENCES Users(UserID);

-- Add foreign key for TeamID in tblUsers
ALTER TABLE Users
ADD CONSTRAINT FK_Users_TeamID FOREIGN KEY (TeamID) REFERENCES Teams(TeamID);
