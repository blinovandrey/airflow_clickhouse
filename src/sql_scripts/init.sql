/*
Выбран Log engine, поскольку позволяет быстро вставлять нестуркурированые данные
и параллельно читать их в дальнейшем
 */
CREATE TABLE raw_data
(
    data String
)
    engine = Log();

/*
Выбран MergeTree engine, поскольку данный движок имеет богатый функионал для работы с структурированными данными.
Позволяет быстро записывать данные по частям, поддерживает сортировку по ключу, партиции, репликацию.
Для строковых полей малой мощности используем функцию LowCardinality, чтобы эффективнее сжимать такие поля.
 */

CREATE TABLE events
(
    ts            DateTime,
    userId        Nullable(UInt16),
    sessionId     Nullable(UInt16),
    page          LowCardinality(Nullable(String)),
    auth          LowCardinality(Nullable(String)),
    method        LowCardinality(Nullable(String)),
    status        Nullable(UInt8),
    level         LowCardinality(Nullable(String)),
    itemInSession Nullable(UInt16),
    location      Nullable(String),
    userAgent     Nullable(String),
    lastName      Nullable(String),
    firstName     Nullable(String),
    registration  Nullable(UInt16),
    gender        LowCardinality(Nullable(String)),
    artist        Nullable(String),
    song          Nullable(String),
    length        Nullable(Float32)
)
    engine = MergeTree ORDER BY ts SETTINGS index_granularity = 8192;
