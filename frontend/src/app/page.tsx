"use client"

import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'

import ParserService from '@/services/parser'

export default function Home() {
  const [sql, setSql] = useState<string>("")

  const modifiedSQL = useMutation({
    mutationFn: async (_sql: string) => {
      return await ParserService.hashedSQLColumns(_sql)
    },
  })

  const mappedHasedColumns = useMutation({
    mutationFn: async (_sql: string) => {
      return await ParserService.mappedHashedColumns(_sql)
    },
  })

  const submitHandler = (e: React.FormEvent) => {
    e.preventDefault()
    modifiedSQL.mutate(sql)
    mappedHasedColumns.mutate(sql)
  }



  return (
    <main className="w-full max-w-[1080px] m-auto pt-20">
      <div className='w-full max-w-[700px] m-auto'>
        <form onSubmit={submitHandler} className='flex flex-col gap-5 w-full'>
          <label htmlFor='sql' className='font-bold'>Insert your SQL code here</label>
          <textarea id="sql" onChange={(e) => setSql(e.target.value)} className='border p-3 w-full h-[300px]' placeholder='ex: SELECT col from table' />
          <input className='bg-teal-500 text-white px-3 py-2 rounded-lg shadow-lg' type="submit" value="Submit" />
        </form>
        <div className='flex flex-col gap-5 mt-7'>
          {!modifiedSQL.isLoading && modifiedSQL.data && (
            <div><p className="font-bold">Modified SQL:</p> <code>{modifiedSQL.data.data.result}</code></div>
          )}
          {!mappedHasedColumns.isLoading && mappedHasedColumns.data && (
            <div><p className="font-bold">Mapped Columns:</p> <pre>{JSON.stringify(mappedHasedColumns.data.data.result, null, 2)}</pre></div>
          )}
        </div>
      </div>

    </main>
  )
}
