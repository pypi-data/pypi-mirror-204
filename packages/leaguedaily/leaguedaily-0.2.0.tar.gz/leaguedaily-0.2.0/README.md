# league-daily

Leauge of Legends Esports update straight from the terminal!

Now you can stay up-to-date with your favorite LoL teams/leagues despite your busy schedule.
# Install

requirement: `python3 >= 3.10`


`pip install leaguedaily`

# Usage

By default, `league-daily` without any arguments will show League of Legends Esports result from the previous day.

<img width="638" alt="Screenshot 2023-04-19 at 8 00 06 PM" src="https://user-images.githubusercontent.com/60205090/233247146-f660c989-8cae-41a2-9360-0c60b13ee694.png">

You can also specify dates in the format of `YYYY-MM-DD` as an argument to the program.

<img width="878" alt="Screenshot 2023-04-19 at 8 05 28 PM" src="https://user-images.githubusercontent.com/60205090/233247879-074f620d-b2fd-4a26-a836-3d853a5ad27b.png">


`--team` flag can be used to specify one or more teams in addition to the given date argument.

<img width="574" alt="Screenshot 2023-04-19 at 8 08 03 PM" src="https://user-images.githubusercontent.com/60205090/233248250-c9a32b79-53be-4f7c-9415-c57f6e85ade5.png">
<img width="730" alt="Screenshot 2023-04-19 at 8 08 51 PM" src="https://user-images.githubusercontent.com/60205090/233248406-3f666713-be6b-4128-aaa3-855db1ef6a4d.png">

`--league` flag can be used to limit the results to only the given leagues.

<img width="859" alt="Screenshot 2023-04-19 at 8 12 15 PM" src="https://user-images.githubusercontent.com/60205090/233248886-ce80d938-f530-43ad-b078-dc7331f52614.png">


# Known problems

1. Data is pulled from leaguepedia, so there is a limit as to how much data a normal user can pull. As a result, given a too-far-away-from-present date, program's result could be truncated or incorrect.
2. A BO3 series could be in the same day in local time, but in UTC (default time when pulled from API), 2 matches are on the same day and 1 match is on the next day (past midnight UTC time, but still the same day local time). 

Given the goal of this project (daily update for some busy fans), I decide not to address these problems. The program works consistently enough for what it is created for.

Cheers! 🎆 
