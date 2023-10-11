import api from "@/utils/requests";

export default class ParserService {
  static baseUrl = "/api/parser";

  public static hashedSQLColumns = async (sql: string) => {
    return api.post(`${this.baseUrl}/columns/hashed`, {
      sql,
    });
  };

  public static mappedHashedColumns = async (
    sql: string
  ) => {
    return api.post(`${this.baseUrl}/columns/mapped`, {
      sql,
    });
  };
}
